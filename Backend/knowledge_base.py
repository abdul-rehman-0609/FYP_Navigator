from typing import List, Dict, Set, Any, Tuple
from dataclasses import dataclass, field
from itertools import product
import random

@dataclass
class TopicRequirement:
    """Requirements for a specific FYP topic."""
    required_skills: Dict[str, int]  # Skill name -> Min proficiency value (1-4)
    min_cgpa: float
    required_courses: Set[str]
    team_size_min: int
    team_size_max: int
    estimated_weekly_hours: int

@dataclass
class TopicTemplate:
    """Template for a Final Year Project topic."""
    id: str
    title: str
    description: str
    domain: str
    technique: str  # NEW: The technique used
    context: str  # NEW: The application context/constraint
    difficulty: str
    requirements: TopicRequirement
    risk_factors: List[str]
    keywords: List[str]

@dataclass
class DomainInfo:
    """Information about a project domain."""
    name: str
    base_skills: Dict[str, int]  # Skills common to this domain
    base_courses: List[str]
    description: str

@dataclass
class TechniqueInfo:
    """Information about a technique/technology."""
    name: str
    required_skills: Dict[str, int]  # Skills needed for this technique
    difficulty: str  # 'Beginner', 'Intermediate', 'Advanced'
    min_cgpa: float
    estimated_hours: int
    risk_factors: List[str]
    description: str

@dataclass
class ContextInfo:
    """Information about an application context/constraint."""
    name: str
    additional_skills: Dict[str, int]  # Extra skills for this context
    additional_courses: List[str]
    complexity_modifier: float  # Multiplier for difficulty (0.8-1.2)
    description: str

class KnowledgeBase:
    """
    Expert knowledge repository with dynamic topic generation.
    Generates topics using: <Domain> + <Technique> + <Context>
    """
    def __init__(self):
        self.topics: Dict[str, TopicTemplate] = {}
        self.domains: Dict[str, DomainInfo] = {}
        self.techniques: Dict[str, TechniqueInfo] = {}
        self.contexts: Dict[str, ContextInfo] = {}
        self._initialize_knowledge()
        self._generate_all_topics()

    def _initialize_knowledge(self):
        """Initialize the knowledge catalogs."""
        self._init_domains()
        self._init_techniques()
        self._init_contexts()

    def _init_domains(self):
        """Define project domains."""
        self.domains = {
            "Web Development": DomainInfo(
                name="Web Development",
                base_skills={"html": 2, "css": 2, "javascript": 2},
                base_courses=["Web Engineering"],
                description="Building web applications and services"
            ),
            "Mobile Development": DomainInfo(
                name="Mobile Development",
                base_skills={"java": 2, "kotlin": 1},
                base_courses=["Mobile Application Development"],
                description="Creating mobile applications for iOS/Android"
            ),
            "Data Science": DomainInfo(
                name="Data Science",
                base_skills={"python": 2, "pandas": 2, "numpy": 2},
                base_courses=["Data Structures", "Statistics"],
                description="Analyzing and extracting insights from data"
            ),
            "Artificial Intelligence": DomainInfo(
                name="Artificial Intelligence",
                base_skills={"python": 2, "mathematics": 2},
                base_courses=["Artificial Intelligence", "Linear Algebra"],
                description="Building intelligent systems and algorithms"
            ),
            "IoT": DomainInfo(
                name="IoT",
                base_skills={"python": 2, "arduino": 1, "sensors": 1},
                base_courses=["Embedded Systems"],
                description="Internet of Things and connected devices"
            ),
            "Cybersecurity": DomainInfo(
                name="Cybersecurity",
                base_skills={"networking": 2, "cryptography": 2},
                base_courses=["Computer Networks", "Information Security"],
                description="Security systems and threat detection"
            ),
            "Game Development": DomainInfo(
                name="Game Development",
                base_skills={"unity": 2, "c#": 2},
                base_courses=["Computer Graphics"],
                description="Creating interactive games and simulations"
            ),
            "Cloud Computing": DomainInfo(
                name="Cloud Computing",
                base_skills={"aws": 1, "docker": 2, "kubernetes": 1},
                base_courses=["Distributed Systems"],
                description="Cloud-based applications and services"
            )
        }

    def _init_techniques(self):
        """Define techniques/technologies."""
        self.techniques = {
            "Machine Learning": TechniqueInfo(
                name="Machine Learning",
                required_skills={"python": 2, "scikit-learn": 2, "pandas": 2},
                difficulty="Intermediate",
                min_cgpa=2.8,
                estimated_hours=18,
                risk_factors=["Data quality issues", "Model training complexity"],
                description="Using ML algorithms for prediction and classification"
            ),
            "Deep Learning": TechniqueInfo(
                name="Deep Learning",
                required_skills={"python": 3, "pytorch": 2, "tensorflow": 2},
                difficulty="Advanced",
                min_cgpa=3.2,
                estimated_hours=22,
                risk_factors=["High computational requirements", "Complex architecture design"],
                description="Neural networks for complex pattern recognition"
            ),
            "Computer Vision": TechniqueInfo(
                name="Computer Vision",
                required_skills={"python": 2, "opencv": 2, "image-processing": 2},
                difficulty="Intermediate",
                min_cgpa=2.9,
                estimated_hours=20,
                risk_factors=["Image quality dependency", "Real-time processing challenges"],
                description="Processing and analyzing visual information"
            ),
            "Natural Language Processing": TechniqueInfo(
                name="Natural Language Processing",
                required_skills={"python": 3, "nlp": 2, "transformers": 2},
                difficulty="Advanced",
                min_cgpa=3.0,
                estimated_hours=20,
                risk_factors=["Language ambiguity", "Context understanding"],
                description="Understanding and generating human language"
            ),
            "Blockchain": TechniqueInfo(
                name="Blockchain",
                required_skills={"solidity": 2, "web3": 2, "cryptography": 2},
                difficulty="Advanced",
                min_cgpa=3.1,
                estimated_hours=19,
                risk_factors=["Security vulnerabilities", "Scalability issues"],
                description="Distributed ledger technology"
            ),
            "Augmented Reality": TechniqueInfo(
                name="Augmented Reality",
                required_skills={"unity": 2, "ar-core": 2, "3d-modeling": 1},
                difficulty="Intermediate",
                min_cgpa=2.7,
                estimated_hours=17,
                risk_factors=["Device compatibility", "Tracking accuracy"],
                description="Overlaying digital content on real world"
            ),
            "Microservices": TechniqueInfo(
                name="Microservices",
                required_skills={"docker": 2, "api-design": 2, "databases": 2},
                difficulty="Intermediate",
                min_cgpa=2.8,
                estimated_hours=16,
                risk_factors=["Service coordination complexity", "Distributed debugging"],
                description="Distributed service architecture"
            ),
            "Real-time Systems": TechniqueInfo(
                name="Real-time Systems",
                required_skills={"websockets": 2, "event-driven": 2, "concurrency": 2},
                difficulty="Advanced",
                min_cgpa=3.0,
                estimated_hours=18,
                risk_factors=["Latency sensitivity", "Concurrency issues"],
                description="Systems with strict timing constraints"
            ),
            "Recommendation Systems": TechniqueInfo(
                name="Recommendation Systems",
                required_skills={"python": 2, "collaborative-filtering": 2, "sql": 2},
                difficulty="Intermediate",
                min_cgpa=2.7,
                estimated_hours=15,
                risk_factors=["Cold start problem", "Data sparsity"],
                description="Personalized content suggestions"
            ),
            "Chatbot Development": TechniqueInfo(
                name="Chatbot Development",
                required_skills={"python": 2, "nlp": 1, "dialog-management": 2},
                difficulty="Beginner",
                min_cgpa=2.5,
                estimated_hours=14,
                risk_factors=["Intent recognition accuracy", "Context management"],
                description="Conversational AI interfaces"
            )
        }

    def _init_contexts(self):
        """Define application contexts/constraints."""
        self.contexts = {
            "E-Commerce Platform": ContextInfo(
                name="E-Commerce Platform",
                additional_skills={"payment-gateway": 1, "inventory": 1},
                additional_courses=["Database Systems"],
                complexity_modifier=1.0,
                description="Online shopping and transaction system"
            ),
            "Healthcare Application": ContextInfo(
                name="Healthcare Application",
                additional_skills={"medical-data": 1, "privacy": 2},
                additional_courses=["Ethics in Computing"],
                complexity_modifier=1.2,
                description="Medical diagnosis and patient management"
            ),
            "Education System": ContextInfo(
                name="Education System",
                additional_skills={"learning-analytics": 1, "assessment": 1},
                additional_courses=[],
                complexity_modifier=0.9,
                description="Learning platforms and educational tools"
            ),
            "Smart City": ContextInfo(
                name="Smart City",
                additional_skills={"iot": 2, "sensors": 2},
                additional_courses=[],
                complexity_modifier=1.1,
                description="Urban infrastructure monitoring and management"
            ),
            "Financial Services": ContextInfo(
                name="Financial Services",
                additional_skills={"financial-modeling": 1, "security": 2},
                additional_courses=["Database Systems"],
                complexity_modifier=1.2,
                description="Banking, trading, and financial analysis"
            ),
            "Social Media Platform": ContextInfo(
                name="Social Media Platform",
                additional_skills={"user-engagement": 1, "content-moderation": 1},
                additional_courses=[],
                complexity_modifier=1.0,
                description="Social networking and content sharing"
            ),
            "Transportation System": ContextInfo(
                name="Transportation System",
                additional_skills={"gps": 2, "routing": 2},
                additional_courses=[],
                complexity_modifier=1.1,
                description="Traffic management and route optimization"
            ),
            "Agriculture Monitoring": ContextInfo(
                name="Agriculture Monitoring",
                additional_skills={"sensors": 2, "data-analysis": 2},
                additional_courses=[],
                complexity_modifier=0.9,
                description="Crop monitoring and farm management"
            ),
            "Environmental Monitoring": ContextInfo(
                name="Environmental Monitoring",
                additional_skills={"sensors": 2, "time-series": 2},
                additional_courses=[],
                complexity_modifier=0.9,
                description="Air quality, water quality, and climate tracking"
            ),
            "Entertainment Platform": ContextInfo(
                name="Entertainment Platform",
                additional_skills={"media-streaming": 1, "content-delivery": 1},
                additional_courses=[],
                complexity_modifier=0.8,
                description="Video/music streaming and content delivery"
            ),
            "Supply Chain Management": ContextInfo(
                name="Supply Chain Management",
                additional_skills={"logistics": 1, "inventory": 2},
                additional_courses=["Database Systems"],
                complexity_modifier=1.0,
                description="Tracking goods from production to delivery"
            ),
            "Customer Service Automation": ContextInfo(
                name="Customer Service Automation",
                additional_skills={"chatbot": 1, "ticketing": 1},
                additional_courses=[],
                complexity_modifier=0.8,
                description="Automated customer support systems"
            ),
            "Security Surveillance": ContextInfo(
                name="Security Surveillance",
                additional_skills={"video-processing": 2, "real-time": 2},
                additional_courses=[],
                complexity_modifier=1.1,
                description="Monitoring and threat detection systems"
            ),
            "Energy Management": ContextInfo(
                name="Energy Management",
                additional_skills={"optimization": 2, "forecasting": 1},
                additional_courses=[],
                complexity_modifier=1.0,
                description="Power consumption monitoring and optimization"
            ),
            "Disaster Response": ContextInfo(
                name="Disaster Response",
                additional_skills={"emergency-systems": 1, "real-time": 2},
                additional_courses=[],
                complexity_modifier=1.2,
                description="Emergency alert and coordination systems"
            )
        }

    def _is_valid_combination(self, domain: str, technique: str, context: str) -> bool:
        """Check if a domain+technique+context combination makes sense."""
        # Define incompatible combinations
        incompatible = {
            ("Game Development", "Blockchain"),
            ("Cybersecurity", "Augmented Reality"),
            ("IoT", "Natural Language Processing"),
        }
        
        if (domain, technique) in incompatible:
            return False
        
        # Some contexts don't work with certain techniques
        if technique == "Blockchain" and context in ["Entertainment Platform", "Education System"]:
            return False
        
        if technique == "Augmented Reality" and context in ["Financial Services", "Supply Chain Management"]:
            return False
        
        return True

    def _generate_all_topics(self):
        """Generate all valid topic combinations."""
        topic_id = 1
        
        for domain_name, domain_info in self.domains.items():
            for technique_name, technique_info in self.techniques.items():
                for context_name, context_info in self.contexts.items():
                    
                    # Check if combination is valid
                    if not self._is_valid_combination(domain_name, technique_name, context_name):
                        continue
                    
                    # Generate topic
                    topic = self._create_topic(
                        topic_id, domain_info, technique_info, context_info
                    )
                    self.topics[topic.id] = topic
                    topic_id += 1

    def _generate_title(self, technique: str, context: str) -> str:
        """Generate varied, natural-sounding titles."""
        # Define title patterns for different techniques
        patterns = {
            "Machine Learning": [
                f"ML-Powered {context}",
                f"Intelligent {context}",
                f"{context} with Predictive Analytics"
            ],
            "Deep Learning": [
                f"Deep Learning-Based {context}",
                f"Neural {context}",
                f"AI-Driven {context}"
            ],
            "Computer Vision": [
                f"Vision-Based {context}",
                f"Image Recognition for {context}",
                f"Visual Intelligence in {context}"
            ],
            "Natural Language Processing": [
                f"NLP-Enhanced {context}",
                f"Language-Aware {context}",
                f"Text Analytics for {context}"
            ],
            "Blockchain": [
                f"Blockchain-Secured {context}",
                f"Decentralized {context}",
                f"Distributed Ledger for {context}"
            ],
            "Augmented Reality": [
                f"AR-Enhanced {context}",
                f"Augmented {context}",
                f"Mixed Reality {context}"
            ],
            "Microservices": [
                f"Microservices-Based {context}",
                f"Scalable {context} Architecture",
                f"Distributed {context}"
            ],
            "Real-time Systems": [
                f"Real-Time {context}",
                f"Live {context}",
                f"Instant {context} Processing"
            ],
            "Recommendation Systems": [
                f"Personalized {context}",
                f"Smart Recommendation for {context}",
                f"Adaptive {context}"
            ],
            "Chatbot Development": [
                f"Conversational {context}",
                f"Chatbot for {context}",
                f"AI Assistant for {context}"
            ]
        }
        
        # Get patterns for this technique, or use default
        technique_patterns = patterns.get(technique, [f"{context} with {technique}"])
        
        # Use hash of context to consistently pick same pattern for same context
        pattern_index = hash(context) % len(technique_patterns)
        return technique_patterns[pattern_index]
    
    def _create_topic(self, topic_id: int, domain: DomainInfo, 
                     technique: TechniqueInfo, context: ContextInfo) -> TopicTemplate:
        """Create a topic from domain, technique, and context."""
        
        # Generate title with varied patterns
        title = self._generate_title(technique.name, context.name)
        
        # Generate description
        description = f"{context.description} implemented with {technique.description.lower()} in the {domain.name.lower()} domain."
        
        # Combine skills
        combined_skills = {}
        combined_skills.update(domain.base_skills)
        combined_skills.update(technique.required_skills)
        combined_skills.update(context.additional_skills)
        
        # Combine courses
        combined_courses = set(domain.base_courses + context.additional_courses)
        
        # Adjust difficulty based on context modifier
        difficulty = technique.difficulty
        hours = int(technique.estimated_hours * context.complexity_modifier)
        cgpa = technique.min_cgpa * context.complexity_modifier
        
        # Create requirements
        requirements = TopicRequirement(
            required_skills=combined_skills,
            min_cgpa=round(cgpa, 2),
            required_courses=combined_courses,
            team_size_min=1,
            team_size_max=3,
            estimated_weekly_hours=hours
        )
        
        # Combine risk factors
        risk_factors = technique.risk_factors + [f"{context.name} domain complexity"]
        
        # Generate keywords
        keywords = [domain.name.lower(), technique.name.lower(), context.name.lower()]
        
        return TopicTemplate(
            id=f"GEN{topic_id:04d}",
            title=title,
            description=description,
            domain=domain.name,
            technique=technique.name,
            context=context.name,
            difficulty=difficulty,
            requirements=requirements,
            risk_factors=risk_factors,
            keywords=keywords
        )

    def get_all_topics(self) -> List[TopicTemplate]:
        """Get all generated topics."""
        return list(self.topics.values())

    def get_topics_by_domain(self, domain: str) -> List[TopicTemplate]:
        """Get topics filtered by domain."""
        return [t for t in self.topics.values() if t.domain.lower() == domain.lower()]

    def get_topics_by_technique(self, technique: str) -> List[TopicTemplate]:
        """Get topics filtered by technique."""
        return [t for t in self.topics.values() if t.technique.lower() == technique.lower()]

    def get_topics_by_context(self, context: str) -> List[TopicTemplate]:
        """Get topics filtered by context."""
        return [t for t in self.topics.values() if t.context.lower() == context.lower()]

    def get_domain_complexity(self, domain: str) -> str:
        """Heuristic for domain complexity."""
        high_complexity = {"Artificial Intelligence", "Cybersecurity", "Cloud Computing"}
        return "High" if domain in high_complexity else "Medium"
    
    def get_total_topic_count(self) -> int:
        """Get total number of generated topics."""
        return len(self.topics)
