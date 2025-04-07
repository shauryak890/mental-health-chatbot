import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBook,
  faQuestionCircle,
  faLightbulb,
  faPhone,
  faGlobe,
  faHandHoldingHeart,
  faUniversity,
  faHeadSideBrain,
  faBookOpen,
  faUserMd,
  faCalendarCheck,
  faBrain
} from '@fortawesome/free-solid-svg-icons';

function Resources() {
  useEffect(() => {
    // Add scroll observer for reveal animations
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, observerOptions);
    
    document.querySelectorAll('.reveal-on-scroll').forEach(element => {
      observer.observe(element);
    });
    
    return () => {
      // Clean up observer on component unmount
      document.querySelectorAll('.reveal-on-scroll').forEach(element => {
        observer.unobserve(element);
      });
    };
  }, []);

  return (
    <div className="resources-container">
      <a href="#main-content" className="skip-to-content">Skip to content</a>
      <div className="navbar">
        <div className="logo">
          <FontAwesomeIcon icon={faBrain} className="logo-icon" />
          MindfulChat
        </div>
        <nav className="nav-links">
          <a href="/">Home</a>
          <a href="/resources" className="active">Resources</a>
          <a href="/chat">Chat</a>
        </nav>
      </div>

      {/* Page Header */}
      <header className="resource-header" id="main-content">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          Mental Health Resources
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="header-subtitle"
        >
          A curated collection of helpful resources, common myths, and answers to frequently asked questions
        </motion.p>
      </header>

      {/* Resources Section */}
      <section className="resources-section">
        <h2 className="section-title reveal-on-scroll">
          <FontAwesomeIcon icon={faHandHoldingHeart} className="section-icon" />
          Helpful Resources
        </h2>
        <p className="section-description reveal-on-scroll">
          Connecting you with professional mental health services and tools to support your journey
        </p>
        
        <div className="resources-grid">
          <div className="resource-card reveal-on-scroll">
            <div className="resource-icon-container">
              <FontAwesomeIcon icon={faPhone} className="resource-icon" />
            </div>
            <div className="resource-content">
              <h3>Crisis Helplines</h3>
              <p>Immediate support when you need someone to talk to</p>
              <ul className="resource-list">
                <li><a href="https://988lifeline.org/" target="_blank" rel="noopener noreferrer">988 Suicide & Crisis Lifeline</a></li>
                <li><a href="https://www.crisistextline.org/" target="_blank" rel="noopener noreferrer">Crisis Text Line</a></li>
                <li><a href="https://www.nami.org/help" target="_blank" rel="noopener noreferrer">NAMI HelpLine</a></li>
              </ul>
            </div>
          </div>

          <div className="resource-card reveal-on-scroll">
            <div className="resource-icon-container">
              <FontAwesomeIcon icon={faGlobe} className="resource-icon" />
            </div>
            <div className="resource-content">
              <h3>Online Resources</h3>
              <p>Comprehensive platforms for mental health education and tools</p>
              <ul className="resource-list">
                <li><a href="https://www.nimh.nih.gov/" target="_blank" rel="noopener noreferrer">National Institute of Mental Health</a></li>
                <li><a href="https://mhanational.org/" target="_blank" rel="noopener noreferrer">Mental Health America</a></li>
                <li><a href="https://www.healthyminds.org/" target="_blank" rel="noopener noreferrer">Healthy Minds Network</a></li>
              </ul>
            </div>
          </div>

          <div className="resource-card reveal-on-scroll">
            <div className="resource-icon-container">
              <FontAwesomeIcon icon={faUniversity} className="resource-icon" />
            </div>
            <div className="resource-content">
              <h3>Campus Resources</h3>
              <p>Support services specifically for students at universities</p>
              <ul className="resource-list">
                <li><a href="#" target="_blank" rel="noopener noreferrer">University Counseling Center</a></li>
                <li><a href="#" target="_blank" rel="noopener noreferrer">Student Wellness Programs</a></li>
                <li><a href="#" target="_blank" rel="noopener noreferrer">Peer Support Networks</a></li>
              </ul>
            </div>
          </div>

          <div className="resource-card reveal-on-scroll">
            <div className="resource-icon-container">
              <FontAwesomeIcon icon={faBookOpen} className="resource-icon" />
            </div>
            <div className="resource-content">
              <h3>Self-Help Resources</h3>
              <p>Tools and techniques for managing your mental health daily</p>
              <ul className="resource-list">
                <li><a href="https://www.calm.com/" target="_blank" rel="noopener noreferrer">Calm - Meditation App</a></li>
                <li><a href="https://www.headspace.com/" target="_blank" rel="noopener noreferrer">Headspace - Mindfulness App</a></li>
                <li><a href="https://www.verywellmind.com/" target="_blank" rel="noopener noreferrer">VeryWell Mind</a></li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Myths Section */}
      <section className="myths-section">
        <h2 className="section-title reveal-on-scroll">
          <FontAwesomeIcon icon={faLightbulb} className="section-icon" />
          Mental Health Myths
        </h2>
        <p className="section-description reveal-on-scroll">
          Dispelling common misconceptions about mental health to promote understanding and reduce stigma
        </p>

        <div className="myths-grid">
          <div className="myth-card reveal-on-scroll">
            <h3>Myth: Mental health problems are uncommon</h3>
            <div className="myth-content">
              <p><strong>Reality:</strong> Mental health conditions are actually very common. Approximately 1 in 5 adults in the U.S. experience mental illness each year, and 1 in 6 youth aged 6-17 experience a mental health disorder annually.</p>
            </div>
          </div>

          <div className="myth-card reveal-on-scroll">
            <h3>Myth: People with mental illness can't handle school or work</h3>
            <div className="myth-content">
              <p><strong>Reality:</strong> Many people with mental health conditions are highly successful students and professionals. With proper support and treatment, mental health conditions can be managed effectively while pursuing educational and career goals.</p>
            </div>
          </div>

          <div className="myth-card reveal-on-scroll">
            <h3>Myth: Mental health problems are a sign of weakness</h3>
            <div className="myth-content">
              <p><strong>Reality:</strong> Mental health conditions are medical conditions, not character flaws or personal weaknesses. They result from a complex interplay of genetic, biological, environmental, and psychological factors – just like many physical health conditions.</p>
            </div>
          </div>

          <div className="myth-card reveal-on-scroll">
            <h3>Myth: You can't help someone with a mental health problem</h3>
            <div className="myth-content">
              <p><strong>Reality:</strong> Friends and family can make a big difference in someone's mental health journey by offering support, encouraging treatment, and helping reduce stigma. Being there for someone and listening without judgment can be incredibly valuable.</p>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="faq-section">
        <h2 className="section-title reveal-on-scroll">
          <FontAwesomeIcon icon={faQuestionCircle} className="section-icon" />
          Frequently Asked Questions
        </h2>
        <p className="section-description reveal-on-scroll">
          Answers to common questions about our chatbot and mental health support
        </p>

        <div className="faq-grid">
          <div className="faq-item reveal-on-scroll">
            <h3>How does MindfulChat work?</h3>
            <p>MindfulChat uses advanced natural language processing to provide supportive conversations tailored to university students. It's designed to listen, provide coping strategies, and direct you to appropriate resources when needed.</p>
          </div>

          <div className="faq-item reveal-on-scroll">
            <h3>Is my conversation with the chatbot private?</h3>
            <p>Absolutely. Your privacy is our priority. Conversations with MindfulChat are confidential and encrypted. We don't share your data with third parties, and you can request to delete your conversation history at any time.</p>
          </div>

          <div className="faq-item reveal-on-scroll">
            <h3>Can the chatbot replace therapy or counseling?</h3>
            <p>No, MindfulChat is not a replacement for professional mental health services. It's designed as a supplementary resource for emotional support and to help connect you with appropriate professional resources when needed.</p>
          </div>

          <div className="faq-item reveal-on-scroll">
            <h3>How do I know if I should seek professional help?</h3>
            <p>Consider seeking professional help if you experience persistent changes in mood, thinking, or behavior that disrupt your daily functioning. This includes feelings of sadness or withdrawal lasting two weeks or more, severe mood swings, excessive fears or worries, or significant changes in eating or sleeping patterns.</p>
          </div>

          <div className="faq-item reveal-on-scroll">
            <h3>How can I support a friend with mental health challenges?</h3>
            <p>Listen without judgment, express concern and support, avoid criticizing or blaming, offer to help them find professional resources, encourage them to continue treatment, and learn about their condition. Most importantly, remember to care for your own wellbeing too.</p>
          </div>

          <div className="faq-item reveal-on-scroll">
            <h3>What should I do in a mental health emergency?</h3>
            <p>If you or someone you know is in immediate danger, call 988 or your local emergency services (911 in the US) right away. For crisis support, text HOME to 741741 to reach the Crisis Text Line, available 24/7.</p>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="about-section">
        <h2 className="section-title reveal-on-scroll">
          <FontAwesomeIcon icon={faBook} className="section-icon" />
          About Mental Health
        </h2>
        <p className="section-description reveal-on-scroll">
          Understanding the fundamentals of mental health and wellbeing
        </p>

        <div className="about-content reveal-on-scroll">
          <div className="about-text">
            <h3>What is mental health?</h3>
            <p>Mental health encompasses our emotional, psychological, and social well-being. It affects how we think, feel, and act, and determines how we handle stress, relate to others, and make choices. Mental health is important at every stage of life, from childhood and adolescence through adulthood.</p>
            
            <h3>Mental health in university students</h3>
            <p>University students face unique challenges that can impact their mental health, including academic pressure, financial stress, social adjustments, and career uncertainty. Research shows that nearly 40% of college students experience a significant mental health issue, yet many don't seek help due to stigma or lack of awareness about available resources.</p>
            
            <h3>The importance of early intervention</h3>
            <p>Addressing mental health concerns early is crucial. Early intervention can prevent issues from worsening, reduce the duration of illness, and improve outcomes. Recognizing changes in thoughts, feelings, or behaviors and seeking support when needed are key steps toward maintaining good mental health.</p>
          </div>
          
          <div className="about-stats">
            <div className="stat-item">
              <div className="stat-number">1 in 4</div>
              <div className="stat-description">people will experience a mental health condition in their lifetime</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">75%</div>
              <div className="stat-description">of mental health conditions develop by age 24</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">60%</div>
              <div className="stat-description">of college students reported feeling overwhelming anxiety</div>
            </div>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <div className="footer-logo">
            <FontAwesomeIcon icon={faBrain} className="logo-icon" />
            MindfulChat
          </div>
          <p className="footer-copyright">© {new Date().getFullYear()} MindfulChat. All rights reserved.</p>
          <p className="footer-disclaimer">MindfulChat is not a replacement for professional mental health services.</p>
        </div>
      </footer>
    </div>
  );
}

export default Resources; 