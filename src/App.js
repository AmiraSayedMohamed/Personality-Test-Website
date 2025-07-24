import React, { useState, useEffect } from 'react';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8005';

function App() {
  const [currentStep, setCurrentStep] = useState('welcome'); // welcome, test, report
  const [session, setSession] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [report, setReport] = useState(null);
  const [userName, setUserName] = useState('');
  const [userGender, setUserGender] = useState('');
  const [userBirthYear, setUserBirthYear] = useState('');
  const [userMaritalStatus, setUserMaritalStatus] = useState('');
  const [userEducationLevel, setUserEducationLevel] = useState('');
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [progress, setProgress] = useState(0);
  const [language, setLanguage] = useState('ar'); // 'ar' for Arabic, 'en' for English

  // Language translations
  const translations = {
    ar: {
      title: 'اختبار الشخصية - نموذج العوامل الخمسة الكبرى',
      welcome: 'مرحباً بك في اختبار الشخصية',
      description: 'سيساعدك هذا الاختبار على فهم شخصيتك بشكل أفضل من خلال تحليل العوامل الخمسة الكبرى للشخصية',
      name: 'الاسم الكامل',
      nameError: 'الرجاء إدخال اسمك',
      gender: 'الجنس',
      male: 'ذكر',
      female: 'أنثى',
      genderError: 'الرجاء اختيار الجنس',
      birthYear: 'سنة الميلاد',
      birthYearError: 'الرجاء إدخال سنة الميلاد',
      maritalStatus: 'الحالة الاجتماعية',
      single: 'أعزب',
      married: 'متزوج',
      divorced: 'مطلق',
      widowed: 'أرمل',
      maritalError: 'الرجاء اختيار الحالة الاجتماعية',
      education: 'المستوى التعليمي',
      middle: 'متوسط',
      high: 'ثانوي',
      diploma: 'دبلوم',
      bachelor: 'جامعي',
      master: 'ماجستير',
      phd: 'دكتوراه',
      educationError: 'الرجاء اختيار المستوى التعليمي',
      startTest: 'ابدأ الاختبار',
      loading: 'جاري التحميل...',
      question: 'سؤال',
      of: 'من',
      stronglyDisagree: 'أرفض بشدة',
      disagree: 'أرفض',
      neutral: 'محايد',
      agree: 'أوافق',
      stronglyAgree: 'أوافق بشدة',
      next: 'التالي',
      finish: 'إنهاء الاختبار',
      yourResults: 'نتائجك',
      personalityReport: 'تقرير الشخصية الخاص بك',
      dimension: 'البعد',
      score: 'النقاط',
      description_trait: 'الوصف',
      newTest: 'اختبار جديد'
    },
    en: {
      title: 'Personality Test - Big Five Model',
      welcome: 'Welcome to the Personality Test',
      description: 'This test will help you understand your personality better through analyzing the Big Five personality factors',
      name: 'Full Name',
      nameError: 'Please enter your name',
      gender: 'Gender',
      male: 'Male',
      female: 'Female',
      genderError: 'Please select gender',
      birthYear: 'Birth Year',
      birthYearError: 'Please enter birth year',
      maritalStatus: 'Marital Status',
      single: 'Single',
      married: 'Married',
      divorced: 'Divorced',
      widowed: 'Widowed',
      maritalError: 'Please select marital status',
      education: 'Education Level',
      middle: 'Middle School',
      high: 'High School',
      diploma: 'Diploma',
      bachelor: 'Bachelor',
      master: 'Master',
      phd: 'PhD',
      educationError: 'Please select education level',
      startTest: 'Start Test',
      loading: 'Loading...',
      question: 'Question',
      of: 'of',
      stronglyDisagree: 'Strongly Disagree',
      disagree: 'Disagree',
      neutral: 'Neutral',
      agree: 'Agree',
      stronglyAgree: 'Strongly Agree',
      next: 'Next',
      finish: 'Finish Test',
      yourResults: 'Your Results',
      personalityReport: 'Your Personality Report',
      dimension: 'Dimension',
      score: 'Score',
      description_trait: 'Description',
      newTest: 'New Test'
    }
  };

  const t = translations[language];

  // Start new test session
  const startTest = async () => {
    if (!userName.trim()) {
      setError(t.nameError);
      return;
    }
    if (!userGender) {
      setError(t.genderError);
      return;
    }
    if (!userBirthYear) {
      setError(t.birthYearError);
      return;
    }
    if (!userEducationLevel) {
      setError(t.educationError);
      return;
    }

    // Calculate age and validate marital status
    const age = 2025 - parseInt(userBirthYear);
    let maritalStatus = userMaritalStatus;
    if (age >= 18 && !maritalStatus) {
      setError(t.maritalError);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${BACKEND_URL}/api/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: userName,
          gender: userGender,
          birth_year: parseInt(userBirthYear),
          marital_status: maritalStatus,
          education_level: userEducationLevel,
          language: language
        })
      });

      if (!response.ok) {
        throw new Error(language === 'ar' ? 'فشل في إنشاء جلسة الاختبار' : 'Failed to create test session');
      }

      const sessionData = await response.json();
      setSession(sessionData);
      setCurrentStep('test');
      await loadCurrentQuestion(sessionData.session_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Load current question
  const loadCurrentQuestion = async (sessionId) => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/sessions/${sessionId}/question`);
      
      if (!response.ok) {
        throw new Error(language === 'ar' ? 'فشل في تحميل السؤال' : 'Failed to load question');
      }

      const questionData = await response.json();
      setCurrentQuestion(questionData);
      setSelectedAnswer(null);
      setProgress((questionData.question_number / 50) * 100);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Submit answer
  const submitAnswer = async () => {
    if (selectedAnswer === null) {
      setError('الرجاء اختيار إجابة');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${BACKEND_URL}/api/answers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: session.session_id,
          question_id: currentQuestion.question_id,
          response: selectedAnswer
        })
      });

      if (!response.ok) {
        throw new Error('فشل في حفظ الإجابة');
      }

      const result = await response.json();
      
      if (result.status === 'completed') {
        // Test completed, load report
        await loadReport();
      } else {
        // Continue to next question
        await loadCurrentQuestion(session.session_id);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Load personality report
  const loadReport = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/sessions/${session.session_id}/report`);
      
      if (!response.ok) {
        throw new Error('فشل في تحميل التقرير');
      }

      const reportData = await response.json();
      setReport(reportData);
      setCurrentStep('report');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Reset test
  const resetTest = () => {
    setCurrentStep('welcome');
    setSession(null);
    setCurrentQuestion(null);
    setReport(null);
    setUserName('');
    setUserGender('');
    setUserBirthYear('');
    setUserMaritalStatus('');
    setUserEducationLevel('');
    setSelectedAnswer(null);
    setProgress(0);
    setError('');
  };

  // Answer scale labels in Arabic and English
  const answerLabels = language === 'ar' ? [
    'غير صحيح تماماً',
    'غير صحيح نوعاً ما',
    'محايد',
    'صحيح نوعاً ما',
    'صحيح تماماً'
  ] : [
    'Strongly Disagree',
    'Disagree',
    'Neutral',
    'Agree',
    'Strongly Agree'
  ];

  return (
    <div className="app" dir={language === 'ar' ? 'rtl' : 'ltr'}>
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <div className="title-section">
              <h1 className="title">{t.title}</h1>
              <p className="subtitle">{t.description}</p>
            </div>
            <button 
              className="language-toggle"
              onClick={() => setLanguage(language === 'ar' ? 'en' : 'ar')}
            >
              {language === 'ar' ? 'English' : 'العربية'}
            </button>
          </div>
        </header>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <div className="error-content">
              <span className="error-icon">⚠️</span>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Welcome Step */}
        {currentStep === 'welcome' && (
          <div className="step-container">
            <div className="welcome-card">
              <div className="welcome-icon">🧠</div>
              <h2 className="welcome-title">{t.welcome}</h2>
              <p className="welcome-description">
                {t.description}
              </p>
              
              <div className="form-group">
                <label className="form-label">{t.name} *</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder={t.name}
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">{t.gender} *</label>
                <select
                  className="form-input"
                  value={userGender}
                  onChange={(e) => setUserGender(e.target.value)}
                >
                  <option value="">{language === 'ar' ? 'اختر الجنس' : 'Select Gender'}</option>
                  <option value="male">{t.male}</option>
                  <option value="female">{t.female}</option>
                </select>
              </div>
              
              <div className="form-group">
                <label className="form-label">{t.birthYear} *</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder={language === 'ar' ? "مثال: 1995" : "Example: 1995"}
                  min="1930"
                  max="2010"
                  value={userBirthYear}
                  onChange={(e) => setUserBirthYear(e.target.value)}
                />
              </div>

              {userBirthYear && (2025 - parseInt(userBirthYear)) >= 18 && (
                <div className="form-group">
                  <label className="form-label">{t.maritalStatus} *</label>
                  <select
                    className="form-input"
                    value={userMaritalStatus}
                    onChange={(e) => setUserMaritalStatus(e.target.value)}
                  >
                    <option value="">{language === 'ar' ? 'اختر الحالة الاجتماعية' : 'Select Marital Status'}</option>
                    <option value="اعزب">{t.single}</option>
                    <option value="متزوج">{t.married}</option>
                    <option value="مطلق">{t.divorced}</option>
                    <option value="ارمل">{t.widowed}</option>
                  </select>
                </div>
              )}

              <div className="form-group">
                <label className="form-label">{t.education} *</label>
                <select
                  className="form-input"
                  value={userEducationLevel}
                  onChange={(e) => setUserEducationLevel(e.target.value)}
                >
                  <option value="">{language === 'ar' ? 'اختر المستوى التعليمي' : 'Select Education Level'}</option>
                  <option value="متوسط">{t.middle}</option>
                  <option value="ثانوي">{t.high}</option>
                  <option value="دبلوم">{t.diploma}</option>
                  <option value="جامعي">{t.bachelor}</option>
                  <option value="ماجستير">{t.master}</option>
                  <option value="دكتوراه">{t.phd}</option>
                </select>
              </div>

              <button
                className="primary-button"
                onClick={startTest}
                disabled={loading}
              >
                {loading ? (
                  <span className="loading-spinner">{t.loading}</span>
                ) : (
                  t.startTest
                )}
              </button>

              <div className="info-cards">
                <div className="info-card">
                  <h3>🎯 دقيق علمياً</h3>
                  <p>مبني على نموذج الشخصية الخماسي المعترف به عالمياً</p>
                </div>
                <div className="info-card">
                  <h3>🤖 تكيفي بالذكاء الاصطناعي</h3>
                  <p>أسئلة مولدة بالذكاء الاصطناعي تتكيف مع إجاباتك</p>
                </div>
                <div className="info-card">
                  <h3>📊 تقرير شامل</h3>
                  <p>تحليل مفصل لشخصيتك مع توصيات للتطوير</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Test Step */}
        {currentStep === 'test' && currentQuestion && (
          <div className="step-container">
            <div className="test-card">
              {/* Progress Bar */}
              <div className="progress-container">
                <div className="progress-info">
                  <span>السؤال {currentQuestion.question_number} من 50</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>

              {/* Question */}
              <div className="question-container">
                <h2 className="question-text">{currentQuestion.text}</h2>
              </div>

              {/* Answer Options */}
              <div className="answers-container">
                <p className="answers-instruction">
                  {language === 'ar' ? 'اختر الإجابة التي تصف شخصيتك بشكل أفضل:' : 'Choose the answer that best describes your personality:'}
                </p>
                <div className="answer-options">
                  {answerLabels.map((label, index) => (
                    <button
                      key={index + 1}
                      className={`answer-option ${selectedAnswer === index + 1 ? 'selected' : ''}`}
                      onClick={() => setSelectedAnswer(index + 1)}
                    >
                      <div className="answer-number">{index + 1}</div>
                      <div className="answer-label">{label}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Navigation */}
              <div className="navigation-container">
                <button
                  className="primary-button"
                  onClick={submitAnswer}
                  disabled={loading || selectedAnswer === null}
                >
                  {loading ? (
                    <span className="loading-spinner">{language === 'ar' ? 'جاري الحفظ...' : 'Saving...'}</span>
                  ) : (
                    currentQuestion.question_number === 50 ? 'إنهاء الاختبار' : 'السؤال التالي'
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Report Step */}
        {currentStep === 'report' && report && (
          <div className="step-container">
            <div className="report-card">
              <div className="report-header">
                <h2 className="report-title">تقرير شخصيتك - {report.name}</h2>
                <p className="report-date">تاريخ الإكمال: {new Date(report.completion_date).toLocaleDateString('ar-SA')}</p>
              </div>

              {/* Scores */}
              <div className="scores-section">
                <h3 className="section-title">نتائج أبعاد الشخصية الخمسة</h3>
                <div className="scores-grid">
                  {Object.entries(report.scores).map(([dimension, data]) => (
                    <div key={dimension} className="score-card">
                      <h4 className="score-dimension">{data.name}</h4>
                      <div className="score-visual">
                        <div className="score-bar">
                          <div 
                            className="score-fill"
                            style={{ width: `${(data.score / 5) * 100}%` }}
                          ></div>
                        </div>
                        <div className="score-info">
                          <span className="score-value">{data.score.toFixed(1)}/5</span>
                          <span className={`score-level ${data.level.toLowerCase()}`}>{data.level}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Detailed Analysis */}
              <div className="analysis-section">
                <h3 className="section-title">التحليل المفصل</h3>
                <div className="analysis-content">
                  {report.detailed_analysis.split('\n').map((paragraph, index) => (
                    paragraph.trim() && <p key={index} className="analysis-paragraph">{paragraph}</p>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div className="recommendations-section">
                <h3 className="section-title">توصيات للتطوير</h3>
                <div className="recommendations-list">
                  {report.recommendations.map((recommendation, index) => (
                    <div key={index} className="recommendation-item">
                      <span className="recommendation-icon">💡</span>
                      <span className="recommendation-text">{recommendation}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="report-actions">
                <button className="secondary-button" onClick={resetTest}>
                  إجراء اختبار جديد
                </button>
                <button 
                  className="primary-button"
                  onClick={() => window.print()}
                >
                  طباعة التقرير
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Loading Overlay */}
        {loading && currentStep !== 'welcome' && (
          <div className="loading-overlay">
            <div className="loading-content">
              <div className="loading-spinner-large"></div>
              <p>جاري المعالجة...</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;