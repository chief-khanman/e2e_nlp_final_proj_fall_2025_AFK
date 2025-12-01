import requests
from pathlib import Path
from bs4 import BeautifulSoup
import json
from typing import List, Dict
import time
from config import config

class DataCollector:
    """Collects data from various sources for the IEP RAG system"""

    def __init__(self):
        self.raw_data_dir = config.RAW_DATA_DIR

    def collect_ooh_data(self) -> List[Dict]:
        """
        Collect occupational data from Bureau of Labor Statistics OOH
        Returns a list of occupation dictionaries
        """
        print("Collecting Occupational Outlook Handbook data...")

        # OOH main categories to scrape
        ooh_categories = [
            "management",
            "business-and-financial",
            "computer-and-information-technology",
            "architecture-and-engineering",
            "life-physical-and-social-science",
            "community-and-social-service",
            "legal",
            "educational-instruction-and-library",
            "arts-and-design-entertainment-sports-and-media",
            "healthcare",
            "healthcare-support",
            "protective-service",
            "food-preparation-and-serving",
            "building-and-grounds-cleaning-and-maintenance",
            "personal-care-and-service",
            "sales",
            "office-and-administrative-support",
            "farming-fishing-and-forestry",
            "construction-and-extraction",
            "installation-maintenance-and-repair",
            "production",
            "transportation-and-material-moving"
        ]

        occupations = []

        for category in ooh_categories:
            try:
                url = f"https://www.bls.gov/ooh/{category}/home.htm"
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find occupation links
                    occupation_links = soup.find_all('a', href=True)

                    for link in occupation_links:
                        href = link.get('href', '')
                        if href.endswith('.htm') and not href.endswith('home.htm'):
                            occupation_url = f"https://www.bls.gov/ooh/{category}/{href}"

                            # Get occupation details
                            occupation_data = self._scrape_occupation_page(occupation_url)
                            if occupation_data:
                                occupations.append(occupation_data)

                            time.sleep(1)  # Be respectful to the server

                print(f"Collected {len(occupations)} occupations from {category}")
                time.sleep(2)

            except Exception as e:
                print(f"Error collecting data for category {category}: {str(e)}")
                continue

        # Save collected data
        output_file = self.raw_data_dir / "ooh_occupations.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(occupations, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(occupations)} occupations to {output_file}")
        return occupations

    def _scrape_occupation_page(self, url: str) -> Dict:
        """Scrape details from an individual occupation page"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract occupation details
            title = soup.find('h1')
            title = title.get_text().strip() if title else ""

            # Extract summary
            summary = soup.find('div', class_='section', id='summary')
            summary_text = summary.get_text().strip() if summary else ""

            # Extract what they do
            what_they_do = soup.find('div', id='what-they-do')
            what_they_do_text = what_they_do.get_text().strip() if what_they_do else ""

            # Extract work environment
            work_environment = soup.find('div', id='work-environment')
            work_environment_text = work_environment.get_text().strip() if work_environment else ""

            # Extract how to become one
            how_to_become = soup.find('div', id='how-to-become-one')
            how_to_become_text = how_to_become.get_text().strip() if how_to_become else ""

            # Extract pay
            pay = soup.find('div', id='pay')
            pay_text = pay.get_text().strip() if pay else ""

            return {
                'title': title,
                'url': url,
                'summary': summary_text,
                'what_they_do': what_they_do_text,
                'work_environment': work_environment_text,
                'how_to_become': how_to_become_text,
                'pay': pay_text
            }

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def create_sample_ooh_data(self):
        """
        Create sample OOH data for common occupations
        Use this if web scraping is not working
        """
        sample_occupations = [
            {
                'title': 'Retail Sales Workers',
                'url': 'https://www.bls.gov/ooh/sales/retail-sales-workers.htm',
                'summary': 'Retail sales workers help customers find products they want and process customers\' payments.',
                'what_they_do': 'Retail sales workers typically do the following: Greet customers and offer assistance. Recommend merchandise based on customer needs. Describe merchandise and explain use, operation, and care of merchandise to customers. Answer customers\' questions. Demonstrate use or operation of merchandise. Receive payment by cash, check, credit cards, or automatic debits.',
                'work_environment': 'Retail sales workers work in stores where they help customers find, select, and purchase products. They typically work evenings and weekends. Most work part time.',
                'how_to_become': 'There are typically no formal education requirements for retail sales workers. Most training is done on the job. Employers look for people who enjoy helping customers and who have good communication skills.',
                'pay': 'The median annual wage for retail sales workers was $30,000. Employment is expected to grow.'
            },
            {
                'title': 'Delivery Truck Drivers and Driver/Sales Workers',
                'url': 'https://www.bls.gov/ooh/transportation-and-material-moving/delivery-truck-drivers-and-driver-sales-workers.htm',
                'summary': 'Delivery truck drivers and driver/sales workers pick up, transport, and drop off packages and small shipments within a local region or urban area.',
                'what_they_do': 'Delivery truck drivers and driver/sales workers typically do the following: Load and unload their cargo. Drive to destinations. Report any incidents they encounter on the road. Follow applicable traffic laws. Inspect their vehicles for mechanical items. Keep their vehicles clean. Driver/sales workers also take orders and collect payments.',
                'work_environment': 'Delivery truck drivers and driver/sales workers drive in all weather conditions. Some drivers work nights, early mornings, and weekends.',
                'how_to_become': 'Delivery truck drivers and driver/sales workers typically need a high school diploma and a driver\'s license. They get on-the-job training. Driver/sales workers also need customer service skills.',
                'pay': 'The median annual wage for delivery truck drivers and driver/sales workers was $37,050.'
            },
            {
                'title': 'Customer Service Representatives',
                'url': 'https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm',
                'summary': 'Customer service representatives interact with customers to handle complaints, process orders, and answer questions.',
                'what_they_do': 'Customer service representatives typically do the following: Listen to and respond to customers\' needs and concerns. Provide information about products and services. Take orders and process returns. Record customer interactions and transactions. Resolve customer complaints or refer them to supervisors. Work with customer service software.',
                'work_environment': 'Customer service representatives work in many industries. Many work in call centers, while others work in retail stores, banks, or insurance companies.',
                'how_to_become': 'Customer service representatives typically need a high school diploma. Training is typically provided on the job. Good communication and problem-solving skills are important.',
                'pay': 'The median annual wage for customer service representatives was $37,780.'
            },
            {
                'title': 'Childcare Workers',
                'url': 'https://www.bls.gov/ooh/personal-care-and-service/childcare-workers.htm',
                'summary': 'Childcare workers attend to children at schools, businesses, residences, and childcare institutions.',
                'what_they_do': 'Childcare workers typically do the following: Supervise and monitor the safety of children. Prepare and organize activities. Help children keep good hygiene. Change diapers of infants and toddlers. Organize activities to help develop coordination, cooperation, and social skills. Keep records of daily activities.',
                'work_environment': 'Childcare workers work in childcare centers, homes, schools, and other settings. The work can be demanding, requiring physical stamina and patience.',
                'how_to_become': 'Education and training requirements vary by setting. Many positions require a high school diploma and on-the-job training. Some states require childcare workers to have certifications.',
                'pay': 'The median annual wage for childcare workers was $28,520.'
            },
            {
                'title': 'Food Service Workers',
                'url': 'https://www.bls.gov/ooh/food-preparation-and-serving/food-and-beverage-serving-and-related-workers.htm',
                'summary': 'Food and beverage serving and related workers take and prepare orders, clear tables, and do other tasks associated with providing food service.',
                'what_they_do': 'Food service workers typically do the following: Greet customers and present menus. Take food and beverage orders. Recommend food and beverages. Serve food and beverages. Prepare itemized checks. Clean tables and work areas. Set up dining areas.',
                'work_environment': 'Food service workers work in restaurants, cafeterias, and other food service establishments. Many work part time, and shifts often include evenings, weekends, and holidays.',
                'how_to_become': 'No formal education is required. Most training is done on the job. Good customer service skills are important.',
                'pay': 'The median annual wage varies by occupation. Many food service workers receive tips in addition to wages.'
            }
        ]

        output_file = self.raw_data_dir / "ooh_occupations.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sample_occupations, f, indent=2, ensure_ascii=False)

        print(f"Created sample OOH data with {len(sample_occupations)} occupations at {output_file}")
        return sample_occupations

    def create_educational_standards(self):
        """Create sample educational standards data"""
        print("Creating educational standards data...")

        standards = {
            "21st_century_skills": [
                {
                    "category": "Communication",
                    "standards": [
                        "Use effective communication skills in various contexts",
                        "Listen actively to understand others' perspectives",
                        "Express ideas clearly in both verbal and written forms",
                        "Adapt communication to different audiences and purposes",
                        "Use appropriate tone, body language, and eye contact"
                    ]
                },
                {
                    "category": "Collaboration",
                    "standards": [
                        "Work effectively in diverse teams",
                        "Demonstrate respect for others' ideas and contributions",
                        "Share responsibilities and work toward common goals",
                        "Resolve conflicts constructively",
                        "Give and receive feedback professionally"
                    ]
                },
                {
                    "category": "Critical Thinking",
                    "standards": [
                        "Analyze and evaluate information from multiple sources",
                        "Make reasoned decisions and solve problems",
                        "Identify patterns and make connections",
                        "Ask relevant questions to deepen understanding",
                        "Consider consequences of decisions"
                    ]
                },
                {
                    "category": "Creativity and Innovation",
                    "standards": [
                        "Generate new ideas and approaches",
                        "Demonstrate flexibility in thinking",
                        "Take calculated risks",
                        "Learn from mistakes and iterate",
                        "Apply knowledge in new contexts"
                    ]
                },
                {
                    "category": "Self-Direction",
                    "standards": [
                        "Set and work toward personal and professional goals",
                        "Manage time effectively",
                        "Demonstrate initiative and self-motivation",
                        "Monitor and evaluate own progress",
                        "Seek help and resources when needed"
                    ]
                },
                {
                    "category": "Social Responsibility",
                    "standards": [
                        "Demonstrate ethical behavior and integrity",
                        "Show respect for diversity and different perspectives",
                        "Contribute positively to community and workplace",
                        "Understand and follow workplace norms and expectations",
                        "Demonstrate reliability and accountability"
                    ]
                },
                {
                    "category": "Technology Literacy",
                    "standards": [
                        "Use technology tools effectively and appropriately",
                        "Navigate digital environments safely",
                        "Use technology to access and evaluate information",
                        "Apply technology to solve problems",
                        "Adapt to new technologies"
                    ]
                },
                {
                    "category": "Career and Life Skills",
                    "standards": [
                        "Understand workplace expectations and culture",
                        "Demonstrate professionalism in appearance and behavior",
                        "Follow safety procedures and guidelines",
                        "Manage personal finances responsibly",
                        "Balance work and personal responsibilities"
                    ]
                }
            ],
            "employability_skills": [
                {
                    "skill": "Attendance and Punctuality",
                    "description": "Arrive to work on time and maintain good attendance",
                    "indicators": [
                        "Arrive on time for scheduled shifts",
                        "Call ahead if unable to attend",
                        "Minimize absences",
                        "Stay for entire shift",
                        "Return from breaks on time"
                    ]
                },
                {
                    "skill": "Workplace Appearance",
                    "description": "Dress appropriately for the workplace",
                    "indicators": [
                        "Wear appropriate clothing for job",
                        "Maintain clean and neat appearance",
                        "Follow dress code policies",
                        "Wear required safety equipment",
                        "Practice good personal hygiene"
                    ]
                },
                {
                    "skill": "Following Directions",
                    "description": "Listen to and follow supervisor instructions",
                    "indicators": [
                        "Listen carefully to instructions",
                        "Ask clarifying questions",
                        "Complete tasks as directed",
                        "Seek help when needed",
                        "Accept feedback and make corrections"
                    ]
                },
                {
                    "skill": "Workplace Safety",
                    "description": "Follow safety rules and procedures",
                    "indicators": [
                        "Follow all safety protocols",
                        "Use equipment properly",
                        "Report safety hazards",
                        "Wear protective equipment",
                        "Keep work area clean and organized"
                    ]
                },
                {
                    "skill": "Quality of Work",
                    "description": "Complete work accurately and thoroughly",
                    "indicators": [
                        "Complete tasks to standard",
                        "Pay attention to detail",
                        "Check work for accuracy",
                        "Take pride in work",
                        "Maintain consistent quality"
                    ]
                },
                {
                    "skill": "Productivity",
                    "description": "Work efficiently and stay on task",
                    "indicators": [
                        "Stay focused on assigned tasks",
                        "Work at appropriate pace",
                        "Minimize distractions",
                        "Complete tasks within time expectations",
                        "Use work time productively"
                    ]
                },
                {
                    "skill": "Interpersonal Skills",
                    "description": "Interact positively with others",
                    "indicators": [
                        "Greet customers and coworkers appropriately",
                        "Use respectful language",
                        "Maintain positive attitude",
                        "Work cooperatively with others",
                        "Handle conflicts appropriately"
                    ]
                },
                {
                    "skill": "Problem-Solving",
                    "description": "Identify and resolve workplace problems",
                    "indicators": [
                        "Recognize when problems occur",
                        "Think of possible solutions",
                        "Ask for help when needed",
                        "Try different approaches",
                        "Learn from mistakes"
                    ]
                }
            ]
        }

        output_file = self.raw_data_dir / "educational_standards.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(standards, f, indent=2, ensure_ascii=False)

        print(f"Created educational standards at {output_file}")
        return standards

    def create_iep_samples(self):
        """Create sample IEP goals and transition planning documents"""
        print("Creating sample IEP data...")

        iep_samples = {
            "postsecondary_goals": {
                "employment_examples": [
                    "After high school, [Student] will obtain full-time employment in [field/industry] that aligns with their interests and abilities.",
                    "After high school, [Student] will obtain part-time employment at [specific workplace] as a [job title].",
                    "After high school, [Student] will participate in supported employment services to obtain competitive integrated employment.",
                    "After high school, [Student] will work at least 20 hours per week in a job related to [career interest]."
                ],
                "education_training_examples": [
                    "After high school, [Student] will complete on-the-job training provided by their employer.",
                    "After high school, [Student] will enroll in a vocational training program to develop skills in [field].",
                    "After high school, [Student] will participate in employer-sponsored training workshops.",
                    "After high school, [Student] will complete a certificate program in [field] at [institution].",
                    "After high school, [Student] will participate in a community-based job training program."
                ],
                "independent_living_examples": [
                    "After high school, [Student] will live independently with minimal supports.",
                    "After high school, [Student] will access community resources for daily living needs.",
                    "After high school, [Student] will use public transportation to access work and community activities."
                ]
            },
            "annual_goals": {
                "employment_skills": [
                    "In [time period], [Student] will demonstrate effective workplace communication skills by greeting customers, listening actively, and responding appropriately in [X] out of [Y] opportunities.",
                    "In [time period], [Student] will complete assigned work tasks following a task list or verbal directions with [X]% accuracy in [Y] out of [Z] trials.",
                    "In [time period], [Student] will demonstrate appropriate workplace behavior by arriving on time, following break schedules, and using respectful language in [X] out of [Y] work sessions.",
                    "In [time period], [Student] will identify and report workplace problems to a supervisor in [X] out of [Y] observed situations."
                ],
                "social_skills": [
                    "In [time period], [Student] will initiate and maintain appropriate conversations with peers and adults by making eye contact, taking turns speaking, and staying on topic in [X] out of [Y] opportunities.",
                    "In [time period], [Student] will accept feedback from supervisors or teachers by listening quietly, asking clarifying questions, and implementing changes in [X] out of [Y] instances.",
                    "In [time period], [Student] will resolve conflicts appropriately by using calm tone, listening to others, and suggesting compromises in [X] out of [Y] conflict situations."
                ],
                "independent_living": [
                    "In [time period], [Student] will use public transportation to travel to and from school/work independently in [X] out of [Y] opportunities.",
                    "In [time period], [Student] will manage personal schedule using a planner or digital calendar with [X]% accuracy.",
                    "In [time period], [Student] will prepare simple meals following recipe cards or visual instructions in [X] out of [Y] attempts."
                ]
            },
            "short_term_objectives": {
                "template": "By [date], [Student] will [specific skill/behavior] in [context] with [criterion for success].",
                "examples": [
                    "By [first quarter], [Student] will greet customers by making eye contact and saying 'Hello, how can I help you?' in 3 out of 5 role-play scenarios.",
                    "By [second quarter], [Student] will greet customers in simulated work settings in 4 out of 5 opportunities.",
                    "By [third quarter], [Student] will greet customers during community-based instruction at actual retail locations in 4 out of 5 opportunities.",
                    "By [fourth quarter], [Student] will greet customers independently during work-based learning experiences in 4 out of 5 opportunities."
                ]
            },
            "transition_services": [
                "Instruction: Direct instruction in workplace skills, social skills, and independent living skills",
                "Related Services: Speech therapy for communication skills, occupational therapy for fine motor skills",
                "Community Experiences: Job shadowing, volunteer work, community-based instruction",
                "Employment Objectives: Career exploration, job training, supported employment",
                "Daily Living Skills: Money management, time management, self-care, transportation",
                "Functional Vocational Evaluation: Interest inventories, aptitude assessments, work samples"
            ],
            "idea_requirements": {
                "age_requirements": "Transition planning must begin no later than age 16, or younger if determined appropriate by the IEP team.",
                "measurable_postsecondary_goals": "IEP must include appropriate measurable postsecondary goals based upon age appropriate transition assessments related to training, education, employment, and where appropriate, independent living skills.",
                "transition_services": "IEP must include transition services needed to assist the child in reaching those goals, including courses of study.",
                "update_requirements": "Postsecondary goals and transition services must be updated annually."
            }
        }

        output_file = self.raw_data_dir / "iep_samples.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(iep_samples, f, indent=2, ensure_ascii=False)

        print(f"Created IEP samples at {output_file}")
        return iep_samples

    def collect_all_data(self):
        """Collect all necessary data for the RAG system"""
        print("Starting data collection...")

        # Create sample data (use this instead of web scraping for reliability)
        self.create_sample_ooh_data()
        self.create_educational_standards()
        self.create_iep_samples()

        print("\nData collection complete!")
        print(f"All data saved to: {self.raw_data_dir}")


if __name__ == "__main__":
    collector = DataCollector()
    collector.collect_all_data()
