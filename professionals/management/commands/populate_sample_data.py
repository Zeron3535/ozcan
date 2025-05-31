from django.core.management.base import BaseCommand
from professionals.models import ExpertType, Specialization, City

class Command(BaseCommand):
    help = 'Populate database with sample expert types, specializations, and cities'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample data...')
        
        # Create Expert Types
        expert_types_data = [
            {'name': 'Doktor', 'icon': 'fas fa-user-md', 'order': 1},
            {'name': 'Psikolog', 'icon': 'fas fa-brain', 'order': 2},
            {'name': 'Öğretmen', 'icon': 'fas fa-chalkboard-teacher', 'order': 3},
            {'name': 'Diyetisyen', 'icon': 'fas fa-apple-alt', 'order': 4},
            {'name': 'Avukat', 'icon': 'fas fa-balance-scale', 'order': 5},
            {'name': 'Danışman', 'icon': 'fas fa-handshake', 'order': 6},
            {'name': 'Eğitmen', 'icon': 'fas fa-graduation-cap', 'order': 7},
            {'name': 'Terapist', 'icon': 'fas fa-heart', 'order': 8},
        ]
        
        created_expert_types = {}
        for et_data in expert_types_data:
            expert_type, created = ExpertType.objects.get_or_create(
                name=et_data['name'],
                defaults={
                    'icon': et_data['icon'],
                    'order': et_data['order'],
                    'is_active': True
                }
            )
            created_expert_types[et_data['name']] = expert_type
            if created:
                self.stdout.write(f'  Created expert type: {expert_type.name}')
            else:
                self.stdout.write(f'  Expert type already exists: {expert_type.name}')
        
        # Create Specializations
        specializations_data = [
            # Doktor specializations
            {'name': 'Genel Pratisyen', 'expert_types': ['Doktor'], 'order': 1},
            {'name': 'Kardiyoloji', 'expert_types': ['Doktor'], 'order': 2},
            {'name': 'Dermatoloji', 'expert_types': ['Doktor'], 'order': 3},
            {'name': 'Pediatri', 'expert_types': ['Doktor'], 'order': 4},
            {'name': 'Jinekologi', 'expert_types': ['Doktor'], 'order': 5},
            {'name': 'Fizik Tedavi', 'expert_types': ['Doktor', 'Terapist'], 'order': 6},
            
            # Psikolog specializations
            {'name': 'Klinik Psikoloji', 'expert_types': ['Psikolog'], 'order': 10},
            {'name': 'Çocuk Psikolojisi', 'expert_types': ['Psikolog'], 'order': 11},
            {'name': 'Aile Danışmanlığı', 'expert_types': ['Psikolog', 'Danışman'], 'order': 12},
            {'name': 'Evlilik Terapisi', 'expert_types': ['Psikolog', 'Terapist'], 'order': 13},
            {'name': 'Travma Terapisi', 'expert_types': ['Psikolog', 'Terapist'], 'order': 14},
            
            # Öğretmen specializations
            {'name': 'Matematik', 'expert_types': ['Öğretmen', 'Eğitmen'], 'order': 20},
            {'name': 'Fen Bilimleri', 'expert_types': ['Öğretmen', 'Eğitmen'], 'order': 21},
            {'name': 'İngilizce', 'expert_types': ['Öğretmen', 'Eğitmen'], 'order': 22},
            {'name': 'Türkçe', 'expert_types': ['Öğretmen', 'Eğitmen'], 'order': 23},
            {'name': 'Tarih', 'expert_types': ['Öğretmen', 'Eğitmen'], 'order': 24},
            {'name': 'Coğrafya', 'expert_types': ['Öğretmen', 'Eğitmen'], 'order': 25},
            
            # Diyetisyen specializations
            {'name': 'Beslenme Danışmanlığı', 'expert_types': ['Diyetisyen', 'Danışman'], 'order': 30},
            {'name': 'Spor Beslenmesi', 'expert_types': ['Diyetisyen'], 'order': 31},
            {'name': 'Çocuk Beslenmesi', 'expert_types': ['Diyetisyen'], 'order': 32},
            {'name': 'Kilo Kontrolü', 'expert_types': ['Diyetisyen'], 'order': 33},
            
            # Avukat specializations
            {'name': 'Aile Hukuku', 'expert_types': ['Avukat'], 'order': 40},
            {'name': 'Ceza Hukuku', 'expert_types': ['Avukat'], 'order': 41},
            {'name': 'İş Hukuku', 'expert_types': ['Avukat'], 'order': 42},
            {'name': 'Gayrimenkul Hukuku', 'expert_types': ['Avukat'], 'order': 43},
            
            # Danışman specializations
            {'name': 'Kariyer Danışmanlığı', 'expert_types': ['Danışman'], 'order': 50},
            {'name': 'İş Danışmanlığı', 'expert_types': ['Danışman'], 'order': 51},
            {'name': 'Finansal Danışmanlık', 'expert_types': ['Danışman'], 'order': 52},
            
            # Terapist specializations
            {'name': 'Fizyoterapi', 'expert_types': ['Terapist'], 'order': 60},
            {'name': 'Konuşma Terapisi', 'expert_types': ['Terapist'], 'order': 61},
            {'name': 'Sanat Terapisi', 'expert_types': ['Terapist'], 'order': 62},
        ]
        
        for spec_data in specializations_data:
            specialization, created = Specialization.objects.get_or_create(
                name=spec_data['name'],
                defaults={
                    'order': spec_data['order'],
                    'is_active': True
                }
            )
            
            # Add expert types to specialization
            for et_name in spec_data['expert_types']:
                if et_name in created_expert_types:
                    specialization.expert_types.add(created_expert_types[et_name])
            
            if created:
                self.stdout.write(f'  Created specialization: {specialization.name}')
            else:
                self.stdout.write(f'  Specialization already exists: {specialization.name}')
        
        # Create Cities
        cities_data = [
            {'name': 'İstanbul', 'order': 1},
            {'name': 'Ankara', 'order': 2},
            {'name': 'İzmir', 'order': 3},
            {'name': 'Bursa', 'order': 4},
            {'name': 'Antalya', 'order': 5},
            {'name': 'Adana', 'order': 6},
            {'name': 'Konya', 'order': 7},
            {'name': 'Gaziantep', 'order': 8},
            {'name': 'Kayseri', 'order': 9},
            {'name': 'Mersin', 'order': 10},
            {'name': 'Eskişehir', 'order': 11},
            {'name': 'Diyarbakır', 'order': 12},
            {'name': 'Samsun', 'order': 13},
            {'name': 'Denizli', 'order': 14},
            {'name': 'Şanlıurfa', 'order': 15},
        ]
        
        for city_data in cities_data:
            city, created = City.objects.get_or_create(
                name=city_data['name'],
                defaults={
                    'order': city_data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  Created city: {city.name}')
            else:
                self.stdout.write(f'  City already exists: {city.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data population completed!'))
        self.stdout.write('\nCreated:')
        self.stdout.write(f'  Expert Types: {ExpertType.objects.count()}')
        self.stdout.write(f'  Specializations: {Specialization.objects.count()}') 
        self.stdout.write(f'  Cities: {City.objects.count()}')
        self.stdout.write('\nYou can now use the dynamic filtering system!')
        self.stdout.write('Visit the admin panel to manage these entries or add professionals.') 