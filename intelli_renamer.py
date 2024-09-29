import google.generativeai as genai
import os
import re
import shutil
import time
from PIL import Image
import google.api_core.exceptions
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def intelli_renamer(api_key, folder_name):
    genai.configure(api_key=api_key)

    def extract_bill_details(response_text):
        date_match = re.search(r"(FY_\d{2}-\d{4})", response_text)
        company_name_match = re.search(r"(n-[\w_]+|\*\*([\w-]+)\*\*)", response_text)
        bill_number_match = re.search(r"(b\d+)", response_text)
        amount_match = re.search(r"(a\d+)", response_text)

        date = date_match.group(1) if date_match else None
        
        if company_name_match:
            if company_name_match.group(1).startswith('**'):
                company_name = company_name_match.group(2)
                company_name = f"n-{company_name.replace('_', '_')}"
            else:
                company_name = company_name_match.group(1)
        else:
            company_name = None
        
        bill_number = bill_number_match.group(1) if bill_number_match else None
        amount = amount_match.group(1) if amount_match else None

        return date, company_name, bill_number, amount

    def prep_image(image_path):
        try:
            image = Image.open(image_path)
            image = image.convert("RGB")
            print(f"Successfully opened image: {image_path}")
            return image
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

    def rename_image_file(old_file_path, new_name, new_folder_path):
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        
        _, extension = os.path.splitext(old_file_path)
        new_file_path = os.path.join(new_folder_path, f"{new_name}{extension}")
        
        counter = 1
        while os.path.isfile(new_file_path):
            new_file_path = os.path.join(new_folder_path, f"{new_name}({counter}){extension}")
            counter += 1
        
        os.rename(old_file_path, new_file_path)
        
        return new_file_path

    def move_file_to_folder(file_path, new_folder_path):
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        shutil.move(file_path, new_folder_path)
        print(f"Moved file to {new_folder_path}")

    def extract_text_from_image(image, prompt):
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        while True:
            try:
                response = model.generate_content([image, prompt])
                return response.text
            except AttributeError as e:
                if "finish_message" in str(e):
                    print(f"{e}. Retrying...")
                    time.sleep(5)
                    continue
                elif "500" in str(e):
                    print("InternalServerError' error. Retrying...")
                    time.sleep(5)
                    continue
                else:
                    print(f"Unexpected error: {e}")
                    raise
            except Exception as e:
                print(f"Error occurred: {e}")
                raise

    prompt = "in this invoice reply me month and year , company name with underscore formatted as company_name (in large and bold text), invoice no. (in 3-6 numerical digit only, append b before invoice no. ) and amount (append a before amount and remove special characters ) of this bill in this format strictly 'FY_MM-YYYY company_name b548952 a2044'"

    input_folder_path = folder_name
    output_folder_path = f'renamed_files/{folder_name}'
    skipped_folder_path = f'skipped_files/{folder_name}'

    while True:
        try:
            for filename in os.listdir(input_folder_path):
                if filename.lower().endswith(('.jpeg', '.jpg', '.png', '.pdf', 'jfif')):
                    image_path = os.path.join(input_folder_path, filename)
                    print(f"Processing image: {image_path}")

                    image = prep_image(image_path)
                    if image:
                        text = extract_text_from_image(image, prompt)
                        print(text)

                        date, company_name, bill_number, amount = extract_bill_details(text)
                        details = []

                        if date:
                            details.append(date)
                        if company_name:
                            details.append(company_name)
                        if bill_number:
                            details.append(bill_number)
                        if amount:
                            details.append(amount)

                        if details:
                            new_file_name = " ".join(details)
                            new_file = rename_image_file(image_path, new_file_name, output_folder_path)
                            print(f"File renamed from {filename} to {new_file}")
                        else:
                            print(f"No valid details found in {filename}. Moving to skipped folder...")
                            move_file_to_folder(image_path, skipped_folder_path)
            break

        except google.api_core.exceptions.InternalServerError as e:
            print(f"InternalServerError encountered: {e}. Restarting the process...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            raise

intelli_renamer('AIzaSyCpVKPJQ7wU2o-glG62Yw9bIN-9EI6q7Ig', 'images')
