from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import random
import json
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for testing
sessions = {}

# Add some sample data for testing the dashboard
def add_sample_data():
    import uuid
    sample_sessions = [
        {
            "session_id": str(uuid.uuid4()),
            "name": "أحمد محمد علي",
            "first_name": "أحمد",
            "gender": "male",
            "age": 25,
            "birth_year": 2000,
            "marital_status": "اعزب",
            "education_level": "جامعي",
            "status": "completed",
            "questions_answered": [{"question_id": f"q{i}", "response": 3} for i in range(1, 51)]
        },
        {
            "session_id": str(uuid.uuid4()),
            "name": "فاطمة أحمد حسن",
            "first_name": "فاطمة",
            "gender": "female",
            "age": 30,
            "birth_year": 1995,
            "marital_status": "متزوج",
            "education_level": "ماجستير",
            "status": "completed",
            "questions_answered": [{"question_id": f"q{i}", "response": 4} for i in range(1, 51)]
        },
        {
            "session_id": str(uuid.uuid4()),
            "name": "محمد سعد إبراهيم",
            "first_name": "محمد",
            "gender": "male",
            "age": 35,
            "birth_year": 1990,
            "marital_status": "متزوج",
            "education_level": "دبلوم",
            "status": "completed",
            "questions_answered": [{"question_id": f"q{i}", "response": 2} for i in range(1, 51)]
        },
        {
            "session_id": str(uuid.uuid4()),
            "name": "عائشة محمود طه",
            "first_name": "عائشة",
            "gender": "female",
            "age": 22,
            "birth_year": 2003,
            "marital_status": "اعزب",
            "education_level": "ثانوي",
            "status": "active",
            "questions_answered": [{"question_id": f"q{i}", "response": 3} for i in range(1, 30)]
        },
        {
            "session_id": str(uuid.uuid4()),
            "name": "يوسف حسام الدين",
            "first_name": "يوسف",
            "gender": "male",
            "age": 45,
            "birth_year": 1980,
            "marital_status": "متزوج",
            "education_level": "دكتوراه",
            "status": "completed",
            "questions_answered": [{"question_id": f"q{i}", "response": 5} for i in range(1, 51)]
        }
    ]
    
    for session in sample_sessions:
        sessions[session["session_id"]] = session

# Add sample data when starting
add_sample_data()

# Data persistence functions
def save_sessions():
    """Save sessions to a JSON file"""
    try:
        with open('sessions_data.json', 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving sessions: {e}")

def load_sessions():
    """Load sessions from JSON file"""
    global sessions
    try:
        if os.path.exists('sessions_data.json'):
            with open('sessions_data.json', 'r', encoding='utf-8') as f:
                sessions = json.load(f)
                print(f"Loaded {len(sessions)} sessions from file")
        else:
            add_sample_data()
            save_sessions()
    except Exception as e:
        print(f"Error loading sessions: {e}")
        add_sample_data()

# Load existing sessions when starting
load_sessions()

# Admin credentials (في التطبيق الحقيقي يجب تشفيرها)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # يمكنك تغييرها

# Store admin sessions
admin_sessions = {}

# Sample questions that will be personalized with multi-language support
base_questions = [
    # Openness Questions (10 questions)
    {
        "question_id": "q1",
        "templates": {
            "ar": "هل تشعر يا {name} أن التفكير في الأفكار المجردة والمفاهيم النظرية أمر ممتع بالنسبة لك؟",
            "en": "Do you feel, {name}, that thinking about abstract ideas and theoretical concepts is enjoyable for you?"
        },
        "dimension": "openness",
        "reverse_scored": False
    },
    {
        "question_id": "q2",
        "templates": {
            "ar": "هل تري يا {name} أنك شخص مبدع ومبتكر في حل المشاكل؟",
            "en": "Do you see yourself, {name}, as a creative and innovative person in solving problems?"
        },
        "dimension": "openness",
        "reverse_scored": False
    },
    {
        "question_id": "q3",
        "templates": {
            "ar": "هل تستمتع يا {name} بتجربة أشياء جديدة وغير مألوفة؟",
            "en": "Do you enjoy, {name}, trying new and unfamiliar things?"
        },
        "dimension": "openness",
        "reverse_scored": False
    },
    {
        "question_id": "q4",
        "templates": {
            "ar": "هل تشعر يا {name} أن لديك خيال واسع وحيوي؟",
            "en": "Do you feel, {name}, that you have a wide and vivid imagination?"
        },
        "dimension": "openness",
        "reverse_scored": False
    },
    {
        "question_id": "q5",
        "templates": {
            "ar": "هل تفضل يا {name} الأعمال الفنية والثقافية على الأعمال العملية؟",
            "en": "Do you prefer, {name}, artistic and cultural works over practical ones?"
        },
        "dimension": "openness",
        "reverse_scored": False
    },
    {
        "question_id": "q6",
        "template": "هل تري يا {name} أنك تحب التعلم والاستطلاع باستمرار؟",
        "dimension": "openness",
        "reverse_scored": False
    },
    {
        "question_id": "q7",
        "template": "هل تشعر يا {name} أنك منفتح على الثقافات والآراء المختلفة؟",
        "dimension": "openness",
        "reverse_scored": False
    },
    {
        "question_id": "q8",
        "template": "هل تفضل يا {name} الروتين والأعمال المألوفة على التجديد؟",
        "dimension": "openness",
        "reverse_scored": True
    },
    {
        "question_id": "q9",
        "template": "هل تري يا {name} أنك تقدر الجمال في الطبيعة والفن؟",
        "dimension": "openness",
        "reverse_scored": False
    },
    {
        "question_id": "q10",
        "template": "هل تشعر يا {name} أنك تحب التفكير في أسئلة فلسفية عميقة؟",
        "dimension": "openness",
        "reverse_scored": False
    },

    # Conscientiousness Questions (10 questions)
    {
        "question_id": "q11",
        "template": "هل تشعر يا {name} أنك شخص منظم جداً في حياتك اليومية؟",
        "dimension": "conscientiousness", 
        "reverse_scored": False
    },
    {
        "question_id": "q12",
        "template": "هل تري يا {name} أنك تلتزم بالمواعيد والخطط بدقة؟",
        "dimension": "conscientiousness",
        "reverse_scored": False
    },
    {
        "question_id": "q13",
        "template": "هل تشعر يا {name} أنك تكمل مهامك دائماً حتى النهاية؟",
        "dimension": "conscientiousness",
        "reverse_scored": False
    },
    {
        "question_id": "q14",
        "template": "هل تري يا {name} أنك تخطط للمستقبل بعناية؟",
        "dimension": "conscientiousness",
        "reverse_scored": False
    },
    {
        "question_id": "q15",
        "template": "هل تشعر يا {name} أنك تحب العمل الجاد والاجتهاد؟",
        "dimension": "conscientiousness",
        "reverse_scored": False
    },
    {
        "question_id": "q16",
        "template": "هل تري يا {name} أنك تؤجل أعمالك المهمة أحياناً؟",
        "dimension": "conscientiousness",
        "reverse_scored": True
    },
    {
        "question_id": "q17",
        "template": "هل تشعر يا {name} أنك دقيق في التفاصيل؟",
        "dimension": "conscientiousness",
        "reverse_scored": False
    },
    {
        "question_id": "q18",
        "template": "هل تري يا {name} أنك تحتفظ بأغراضك مرتبة ونظيفة؟",
        "dimension": "conscientiousness",
        "reverse_scored": False
    },
    {
        "question_id": "q19",
        "template": "هل تشعر يا {name} أنك تتحمل المسؤولية بجدية؟",
        "dimension": "conscientiousness",
        "reverse_scored": False
    },
    {
        "question_id": "q20",
        "template": "هل تري يا {name} أنك تضع أهدافاً واضحة لنفسك؟",
        "dimension": "conscientiousness",
        "reverse_scored": False
    },

    # Extraversion Questions (10 questions)
    {
        "question_id": "q21",
        "template": "هل تري يا {name} أن التفاعل مع الآخرين في الأنشطة الاجتماعية شيء مريح لك؟",
        "dimension": "extraversion",
        "reverse_scored": False
    },
    {
        "question_id": "q22",
        "template": "هل تشعر يا {name} أنك شخص نشيط ومليء بالطاقة؟",
        "dimension": "extraversion",
        "reverse_scored": False
    },
    {
        "question_id": "q23",
        "template": "هل تري يا {name} أنك تحب أن تكون مركز الانتباه؟",
        "dimension": "extraversion",
        "reverse_scored": False
    },
    {
        "question_id": "q24",
        "template": "هل تشعر يا {name} أنك تتكلم كثيراً مع الآخرين؟",
        "dimension": "extraversion",
        "reverse_scored": False
    },
    {
        "question_id": "q25",
        "template": "هل تري يا {name} أنك تفضل التجمعات الكبيرة على الجلسات الصغيرة؟",
        "dimension": "extraversion",
        "reverse_scored": False
    },
    {
        "question_id": "q26",
        "template": "هل تشعر يا {name} أنك خجول في المواقف الاجتماعية؟",
        "dimension": "extraversion",
        "reverse_scored": True
    },
    {
        "question_id": "q27",
        "template": "هل تري يا {name} أنك تشعر بالراحة عند مقابلة أشخاص جدد؟",
        "dimension": "extraversion",
        "reverse_scored": False
    },
    {
        "question_id": "q28",
        "template": "هل تشعر يا {name} أنك تحب المغامرة والإثارة؟",
        "dimension": "extraversion",
        "reverse_scored": False
    },
    {
        "question_id": "q29",
        "template": "هل تري يا {name} أنك تفضل قضاء الوقت وحدك؟",
        "dimension": "extraversion",
        "reverse_scored": True
    },
    {
        "question_id": "q30",
        "template": "هل تشعر يا {name} أنك متفائل ومبهج معظم الوقت؟",
        "dimension": "extraversion",
        "reverse_scored": False
    },

    # Agreeableness Questions (10 questions)
    {
        "question_id": "q31",
        "template": "هل تجد يا {name} أنك تثق بالناس بسهولة؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },
    {
        "question_id": "q32",
        "template": "هل تري يا {name} أنك شخص متعاطف مع مشاعر الآخرين؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },
    {
        "question_id": "q33",
        "template": "هل تشعر يا {name} أنك تساعد الآخرين دون انتظار مقابل؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },
    {
        "question_id": "q34",
        "template": "هل تري يا {name} أنك تتجنب الصراعات والخلافات؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },
    {
        "question_id": "q35",
        "template": "هل تشعر يا {name} أنك تقدر وجهات نظر الآخرين حتى لو اختلفت معها؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },
    {
        "question_id": "q36",
        "template": "هل تري يا {name} أنك تشك في نوايا الآخرين أحياناً؟",
        "dimension": "agreeableness",
        "reverse_scored": True
    },
    {
        "question_id": "q37",
        "template": "هل تشعر يا {name} أنك لطيف ومهذب في تعاملك مع الناس؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },
    {
        "question_id": "q38",
        "template": "هل تري يا {name} أنك تحب التعاون أكثر من المنافسة؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },
    {
        "question_id": "q39",
        "template": "هل تشعر يا {name} أنك تغفر للآخرين بسهولة؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },
    {
        "question_id": "q40",
        "template": "هل تري يا {name} أنك متواضع ولا تتفاخر بإنجازاتك؟",
        "dimension": "agreeableness",
        "reverse_scored": False
    },

    # Neuroticism Questions (10 questions)
    {
        "question_id": "q41",
        "template": "هل تشعر يا {name} أنك تقلق كثيراً من الأشياء؟",
        "dimension": "neuroticism",
        "reverse_scored": False
    },
    {
        "question_id": "q42",
        "template": "هل تري يا {name} أن مزاجك يتغير بسرعة؟",
        "dimension": "neuroticism",
        "reverse_scored": False
    },
    {
        "question_id": "q43",
        "template": "هل تشعر يا {name} بالتوتر في المواقف الصعبة؟",
        "dimension": "neuroticism",
        "reverse_scored": False
    },
    {
        "question_id": "q44",
        "template": "هل تري يا {name} أنك تشعر بالحزن أو الاكتئاب أحياناً؟",
        "dimension": "neuroticism",
        "reverse_scored": False
    },
    {
        "question_id": "q45",
        "template": "هل تشعر يا {name} أنك حساس للنقد من الآخرين؟",
        "dimension": "neuroticism",
        "reverse_scored": False
    },
    {
        "question_id": "q46",
        "template": "هل تري يا {name} أنك هادئ ومسترخي معظم الوقت؟",
        "dimension": "neuroticism",
        "reverse_scored": True
    },
    {
        "question_id": "q47",
        "template": "هل تشعر يا {name} أنك تتعامل مع الضغوط بصعوبة؟",
        "dimension": "neuroticism",
        "reverse_scored": False
    },
    {
        "question_id": "q48",
        "template": "هل تري يا {name} أنك تشعر بالغضب بسهولة؟",
        "dimension": "neuroticism",
        "reverse_scored": False
    },
    {
        "question_id": "q49",
        "template": "هل تشعر يا {name} أنك تخاف من المستقبل والمجهول؟",
        "dimension": "neuroticism",
        "reverse_scored": False
    },
    {
        "question_id": "q50",
        "template": "هل تري يا {name} أنك واثق من نفسك في معظم الأوقات؟",
        "dimension": "neuroticism",
        "reverse_scored": True
    }
]

# Pydantic models
class SessionCreate(BaseModel):
    name: str
    gender: str  # "male" or "female"
    birth_year: int
    marital_status: Optional[str] = None  # Will be set based on age
    education_level: str  # "متوسط", "ثانوي", "دبلوم", "جامعي", "ماجستير", "دكتوراه"
    language: Optional[str] = "ar"  # "ar" for Arabic, "en" for English

class SessionResponse(BaseModel):
    session_id: str
    name: str
    status: str
    current_dimension: str
    current_question_number: int
    total_dimensions: int
    dimension_progress: Dict[str, int]

class Question(BaseModel):
    question_id: str
    text: str
    dimension: str
    question_number: int
    reverse_scored: bool = False

class AnswerSubmission(BaseModel):
    session_id: str
    question_id: str
    response: int

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminSession(BaseModel):
    admin_id: str
    username: str
    login_time: str

@app.post("/api/sessions", response_model=SessionResponse)
async def create_session(session_data: SessionCreate):
    try:
        session_id = str(uuid.uuid4())
        
        # Calculate age and determine marital status options
        current_year = 2025
        age = current_year - session_data.birth_year
        
        # If under 18, default to single
        marital_status = session_data.marital_status
        if age < 18:
            marital_status = "اعزب"
        
        # Get first name for personalization
        first_name = session_data.name.split()[0]
        
        # Create session
        sessions[session_id] = {
            "session_id": session_id,
            "name": session_data.name,
            "first_name": first_name,
            "gender": session_data.gender,
            "age": age,
            "birth_year": session_data.birth_year,
            "marital_status": marital_status,
            "education_level": session_data.education_level,
            "language": session_data.language or "ar",
            "status": "active",
            "current_dimension": "openness",
            "current_question_number": 1,
            "questions_answered": [],
            "current_question_index": 0
        }
        
        # Save sessions when a new session is created
        save_sessions()
        
        return SessionResponse(
            session_id=session_id,
            name=session_data.name,
            status="active",
            current_dimension="openness",
            current_question_number=1,
            total_dimensions=5,
            dimension_progress={
                "openness": 0,
                "conscientiousness": 0,
                "extraversion": 0,
                "agreeableness": 0,
                "neuroticism": 0
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")

@app.get("/api/sessions/{session_id}/question", response_model=Question)
async def get_current_question(session_id: str):
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[session_id]
        question_index = session["current_question_index"]
        
        if question_index >= len(base_questions):
            # Test is complete
            raise HTTPException(status_code=404, detail="No more questions")
        
        question_template = base_questions[question_index]
        
        # Get user's language preference
        user_language = session.get("language", "ar")
        
        # Get the appropriate template based on language
        if "templates" in question_template:
            template_text = question_template["templates"].get(user_language, question_template["templates"]["ar"])
        else:
            # Fallback for old format
            template_text = question_template.get("template", "")
        
        # Personalize the question with the user's first name
        personalized_text = template_text.format(
            name=session["first_name"]
        )
        
        return Question(
            question_id=question_template["question_id"],
            text=personalized_text,
            dimension=question_template["dimension"],
            question_number=question_index + 1,
            reverse_scored=question_template["reverse_scored"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting question: {str(e)}")

@app.post("/api/answers")
async def submit_answer(answer: AnswerSubmission):
    try:
        print(f"Received answer: {answer}")
        
        if answer.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[answer.session_id]
        
        # Record the answer
        session["questions_answered"].append({
            "question_id": answer.question_id,
            "response": answer.response
        })
        
        # Move to next question
        session["current_question_index"] += 1
        session["current_question_number"] += 1
        
        print(f"Updated session: {session}")
        
        # Check if test is complete
        if session["current_question_index"] >= len(base_questions):
            session["status"] = "completed"
            print("Test completed!")
            # Save sessions when a test is completed
            save_sessions()
        
        return {"message": "Answer submitted successfully", "status": session["status"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting answer: {str(e)}")

@app.get("/api/sessions/{session_id}/report")
async def get_report(session_id: str):
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = sessions[session_id]
        
        if session["status"] != "completed":
            raise HTTPException(status_code=400, detail="Test not completed yet")
        
        # Generate a simple mock report
        def get_level(score):
            if score >= 80:
                return "عالي"
            elif score >= 60:
                return "متوسط"
            else:
                return "منخفض"
        
        openness_score = random.randint(30, 100)
        conscientiousness_score = random.randint(30, 100)
        extraversion_score = random.randint(30, 100)
        agreeableness_score = random.randint(30, 100)
        neuroticism_score = random.randint(30, 100)
        
        return {
            "session_id": session_id,
            "name": session["name"],
            "completion_date": "2025-01-24T10:30:00Z",
            "scores": {
                "openness": {
                    "name": "الانفتاح على التجارب",
                    "score": openness_score / 20.0,  # Convert to 1-5 scale
                    "level": get_level(openness_score)
                },
                "conscientiousness": {
                    "name": "الضمير الحي",
                    "score": conscientiousness_score / 20.0,
                    "level": get_level(conscientiousness_score)
                },
                "extraversion": {
                    "name": "الانبساط",
                    "score": extraversion_score / 20.0,
                    "level": get_level(extraversion_score)
                },
                "agreeableness": {
                    "name": "المقبولية",
                    "score": agreeableness_score / 20.0,
                    "level": get_level(agreeableness_score)
                },
                "neuroticism": {
                    "name": "العصابية",
                    "score": neuroticism_score / 20.0,
                    "level": get_level(neuroticism_score)
                }
            },
            "detailed_analysis": "تحليل شخصيتك يُظهر توازناً جيداً في معظم الأبعاد.\n\nأنت شخص منفتح على التجارب الجديدة ولديك مستوى جيد من التنظيم والانضباط.\n\nتتمتع بمهارات اجتماعية جيدة وتستطيع التعامل مع الآخرين بطريقة إيجابية.\n\nبشكل عام، شخصيتك متوازنة وتُظهر قدرة على التكيف مع المواقف المختلفة.",
            "recommendations": [
                "استمر في تطوير نقاط قوتك",
                "اعمل على تحسين المجالات التي تحتاج لتطوير",
                "تذكر أن الشخصية قابلة للنمو والتطوير"
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Personality Test API is running"}

# Admin Authentication Endpoints
@app.post("/api/admin/login")
async def admin_login(login_data: AdminLogin):
    try:
        if login_data.username == ADMIN_USERNAME and login_data.password == ADMIN_PASSWORD:
            admin_id = str(uuid.uuid4())
            from datetime import datetime
            
            admin_sessions[admin_id] = {
                "admin_id": admin_id,
                "username": login_data.username,
                "login_time": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "admin_id": admin_id,
                "message": "تم تسجيل الدخول بنجاح"
            }
        else:
            raise HTTPException(status_code=401, detail="بيانات دخول خاطئة")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في تسجيل الدخول: {str(e)}")

@app.get("/api/admin/dashboard/{admin_id}")
async def get_dashboard_data(admin_id: str):
    try:
        # التحقق من صحة جلسة الإدارة
        if admin_id not in admin_sessions:
            raise HTTPException(status_code=401, detail="جلسة غير صالحة")
        
        # حساب الإحصائيات
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions.values() if s["status"] == "completed"])
        active_sessions = len([s for s in sessions.values() if s["status"] == "active"])
        
        # توزيع الأعمار
        ages = [s["age"] for s in sessions.values()]
        age_distribution = {
            "18-25": len([age for age in ages if 18 <= age <= 25]),
            "26-35": len([age for age in ages if 26 <= age <= 35]),
            "36-45": len([age for age in ages if 36 <= age <= 45]),
            "46-55": len([age for age in ages if 46 <= age <= 55]),
            "56+": len([age for age in ages if age > 55])
        }
        
        # توزيع الجنس
        genders = [s["gender"] for s in sessions.values()]
        gender_distribution = {
            "male": genders.count("male"),
            "female": genders.count("female")
        }
        
        # توزيع التعليم
        education_levels = [s["education_level"] for s in sessions.values()]
        education_distribution = {}
        for level in education_levels:
            education_distribution[level] = education_distribution.get(level, 0) + 1
        
        # أحدث المشاركين
        recent_sessions = []
        for session in list(sessions.values())[-5:]:  # آخر 5 مشاركين
            recent_sessions.append({
                "name": session["name"],
                "age": session["age"],
                "gender": session["gender"],
                "status": session["status"],
                "questions_answered": len(session["questions_answered"])
            })
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "active_sessions": active_sessions,
            "completion_rate": round((completed_sessions / total_sessions * 100) if total_sessions > 0 else 0, 1),
            "age_distribution": age_distribution,
            "gender_distribution": gender_distribution,
            "education_distribution": education_distribution,
            "recent_sessions": recent_sessions
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في جلب بيانات الداشبورد: {str(e)}")

@app.get("/api/admin/detailed-reports/{admin_id}")
async def get_detailed_reports(admin_id: str):
    try:
        # التحقق من صحة جلسة الإدارة
        if admin_id not in admin_sessions:
            raise HTTPException(status_code=401, detail="جلسة غير صالحة")
        
        detailed_reports = []
        for session in sessions.values():
            if session["status"] == "completed":
                detailed_reports.append({
                    "session_id": session["session_id"],
                    "name": session["name"],
                    "age": session["age"],
                    "gender": session["gender"],
                    "education_level": session["education_level"],
                    "marital_status": session["marital_status"],
                    "total_questions": len(session["questions_answered"]),
                    "completion_date": "2025-01-24"  # يمكن إضافة التاريخ الحقيقي لاحقاً
                })
        
        return {"detailed_reports": detailed_reports}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في جلب التقارير التفصيلية: {str(e)}")

@app.post("/api/admin/logout/{admin_id}")
async def admin_logout(admin_id: str):
    try:
        if admin_id in admin_sessions:
            del admin_sessions[admin_id]
            return {"success": True, "message": "تم تسجيل الخروج بنجاح"}
        else:
            raise HTTPException(status_code=401, detail="جلسة غير صالحة")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في تسجيل الخروج: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Personality Test API on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
