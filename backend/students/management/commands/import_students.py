# students/management/commands/import_students.py
import csv
import os
import json
import random
import pandas as pd
from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from students.models import Student

class Command(BaseCommand):
    help = 'Import students from a CSV or generate a CSV file with sample student data'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='?', type=str, help='Optional: The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        if not csv_file:
            csv_file = self.generate_sample_csv()

        if csv_file.lower().endswith('.csv'):
            self.import_from_csv(csv_file)
        elif csv_file.lower().endswith('.json'):
            self.import_from_json(csv_file)
        else:
            raise CommandError('Unsupported file format. Please provide a CSV or JSON file.')

        self.stdout.write(self.style.SUCCESS('Successfully imported students'))

    def generate_sample_csv(self):
        csv_file_path = 'sample_students.csv'
        self.stdout.write(self.style.SUCCESS("generate sample csv "))
        fake = Faker()
        if os.path.exists(csv_file_path):
            df = pd.DataFrame(columns = ['name','total_marks'])
            if not df.empty:
                return csv_file_path

        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'total_marks'])

            for i in range(1, 11):
                name = fake.name()
                total_marks = random.randint(60, 100)
                writer.writerow([name, total_marks])

        return csv_file_path

    def import_from_csv(self, csv_file):
        try:
            with open(csv_file, newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    _, created = Student.objects.get_or_create(
                        name=row[0],
                        total_marks=row[1]
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added student {row[0]}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Student {row[0]} already exists'))
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file}" does not exist')

    def import_from_json(self, json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                for student_data in data:
                    _, created = Student.objects.get_or_create(
                        name=student_data['name'],
                        total_marks=student_data['total_marks']
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added student {student_data["name"]}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Student {student_data["name"]} already exists'))
        except FileNotFoundError:
            raise CommandError(f'File "{json_file}" does not exist')
