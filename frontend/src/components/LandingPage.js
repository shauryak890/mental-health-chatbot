import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faMoneyBill, 
  faBook, 
  faUsers, 
  faBrain,
  faHeartPulse,
  faShieldHeart,
  faComments,
  faGraduationCap,
  faClock,
  faHandHoldingHeart,
  faLightbulb,
  faShieldAlt,
  faUserGraduate,
  faChartLine,
  faLaptopCode,
  faMedal,
  faPuzzlePiece,
  faHandshakeAngle,
  faRocket,
  faShieldHalved,
  faHeadset
} from '@fortawesome/free-solid-svg-icons';

function LandingPage({ onStartChat }) {
  const fadeIn = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  };

  useEffect(() => {
    const cards = document.querySelectorAll('.feature-card, .stat-item, .about-feature');
    
    const handleMouseMove = (e) => {
      const card = e.currentTarget;
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    };

    const handleMouseLeave = (e) => {
      const card = e.currentTarget;
      card.style.setProperty('--mouse-x', '50%');
      card.style.setProperty('--mouse-y', '50%');
    };

    cards.forEach(card => {
      card.addEventListener('mousemove', handleMouseMove);
      card.addEventListener('mouseleave', handleMouseLeave);
    });

    return () => {
      cards.forEach(card => {
        card.removeEventListener('mousemove', handleMouseMove);
        card.removeEventListener('mouseleave', handleMouseLeave);
      });
    };
  }, []);

  return (
    <div className="landing-container">
      <nav className="navbar">
        <motion.div 
          className="logo"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <FontAwesomeIcon icon={faHeartPulse} className="logo-icon" />
          MindfulChat
        </motion.div>
        <motion.button 
          className="start-chat-button"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onStartChat}
        >
          Start Chat
        </motion.button>
      </nav>

      <section className="hero-section">
        <motion.div className="hero-content" {...fadeIn}>
          <h1>Your Mental Health Matters</h1>
          <p>A safe, confidential space for university students to find support, guidance, and understanding</p>
          <motion.button 
            className="primary-button"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onStartChat}
          >
            <FontAwesomeIcon icon={faComments} className="button-icon" />
            Chat With Us Now
          </motion.button>
        </motion.div>
        <motion.div 
          className="hero-stats"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="stat-item">
            <div className="icon-container">
              <FontAwesomeIcon icon={faUsers} className="stat-icon" />
            </div>
            <h3>24/7 Support</h3>
            <p>Always here when you need us</p>
          </div>
          <div className="stat-item">
            <FontAwesomeIcon icon={faShieldHeart} className="stat-icon" />
            <h3>100% Confidential</h3>
            <p>Your privacy is our priority</p>
          </div>
          <div className="stat-item">
            <FontAwesomeIcon icon={faGraduationCap} className="stat-icon" />
            <h3>Student-Focused</h3>
            <p>Tailored for university life</p>
          </div>
        </motion.div>
      </section>

      <section className="features-section">
        <motion.h2 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          How We Can Help
        </motion.h2>
        <div className="features-grid">
          {[
            {
              icon: faMoneyBill,
              title: "Financial Stress",
              description: "Navigate financial challenges with guidance on scholarships, budgeting, and financial aid resources",
              secondaryIcons: [faChartLine, faRocket]
            },
            {
              icon: faBook,
              title: "Academic Pressure",
              description: "Develop effective study strategies and manage academic stress with personalized support",
              secondaryIcons: [faLaptopCode, faMedal]
            },
            {
              icon: faUsers,
              title: "Social Connection",
              description: "Build meaningful relationships and overcome feelings of isolation in university life",
              secondaryIcons: [faHandshakeAngle, faPuzzlePiece]
            },
            {
              icon: faBrain,
              title: "Mental Wellness",
              description: "Learn practical techniques for stress management, anxiety relief, and emotional balance",
              secondaryIcons: [faShieldHalved, faHeadset]
            }
          ].map((feature, index) => (
            <motion.div 
              key={index}
              className="feature-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5, transition: { duration: 0.2 } }}
            >
              <div className="feature-card-icons">
                <FontAwesomeIcon icon={feature.icon} className="feature-icon main-icon" />
                <div className="secondary-icons">
                  {feature.secondaryIcons.map((icon, i) => (
                    <FontAwesomeIcon key={i} icon={icon} className="feature-icon secondary-icon" />
                  ))}
                </div>
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="about-section">
        <motion.div 
          className="about-content"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <h2>Empowering Student Wellness</h2>
          <p>
            At MindfulChat, we understand the unique challenges of university life. 
            Our AI-powered platform combines cutting-edge technology with empathetic 
            support to provide you with instant, personalized guidance whenever you need it.
          </p>
          
          <div className="about-features">
            <motion.div 
              className="about-feature"
              whileHover={{ y: -10 }}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <div className="icon-container">
                <FontAwesomeIcon 
                  icon={faClock} 
                  className="about-feature-icon"
                />
              </div>
              <h4>24/7 Availability</h4>
              <p>Access support anytime, anywhere. We're here for you around the clock, ensuring you never feel alone in your journey.</p>
            </motion.div>

            <motion.div 
              className="about-feature"
              whileHover={{ y: -10 }}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.4 }}
            >
              <FontAwesomeIcon 
                icon={faHandHoldingHeart} 
                className="about-feature-icon"
                style={{ display: 'block', marginBottom: '1rem' }}
              />
              <h4>Personalized Care</h4>
              <p>Experience support tailored to your unique situation, with adaptive responses that understand your specific needs.</p>
            </motion.div>

            <motion.div 
              className="about-feature"
              whileHover={{ y: -10 }}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.6 }}
            >
              <FontAwesomeIcon 
                icon={faShieldAlt} 
                className="about-feature-icon"
                style={{ display: 'block', marginBottom: '1rem' }}
              />
              <h4>Safe Space</h4>
              <p>Your privacy and security are our top priorities. Feel confident sharing your thoughts in a completely confidential environment.</p>
            </motion.div>
          </div>

          <motion.div 
            className="about-stats"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.8 }}
          >
            {/* Add any additional statistics or information here */}
          </motion.div>
        </motion.div>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h3>Emergency Contacts</h3>
            <p>National Crisis Hotline: 988</p>
            <p>University Counseling: (XXX) XXX-XXXX</p>
            <p>Emergency Services: 911</p>
          </div>
          <div className="footer-section">
            <h3>Quick Links</h3>
            <p>Mental Health Resources</p>
            <p>Student Support Services</p>
            <p>Wellness Programs</p>
          </div>
          <div className="footer-section">
            <h3>Connect With Us</h3>
            <p>Email: support@mindfulchat.com</p>
            <p>Privacy Policy</p>
            <p>Terms of Service</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2024 MindfulChat. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage; 