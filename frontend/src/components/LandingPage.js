import React, { useEffect, useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faMoneyBillWave,
  faBook, 
  faUserFriends, 
  faBrain,
  faHeartPulse,
  faShieldHeart,
  faComments,
  faArrowRight,
  faCalendarCheck,
  faHandHoldingHeart,
  faLightbulb,
  faGraduationCap,
  faPuzzlePiece,
  faRocket,
  faMountain,
  faCompass
} from '@fortawesome/free-solid-svg-icons';
import mentalWellnessSvg from '../images/mental-wellness.svg';

function LandingPage({ onStartChat }) {
  // Animation variants
  const fadeIn = {
    initial: { opacity: 0, y: 10 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.5 }
  };
  
  // Parallax refs and effects
  const featuresRef = useRef(null);
  const benefitsRef = useRef(null);
  const heroRef = useRef(null);
  const ctaRef = useRef(null);
  
  // Scroll animations
  const { scrollY, scrollYProgress } = useScroll();
  const heroY = useTransform(scrollY, [0, 500], [0, -150]);
  const heroOpacity = useTransform(scrollY, [0, 300], [1, 0.5]);
  
  // Interactive cursor effect
  useEffect(() => {
    const handleMouseMove = (e) => {
      const cards = document.querySelectorAll('.feature-card, .benefit-card');
      const x = e.clientX;
      const y = e.clientY;
      
      cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        // Calculate distance from mouse to card center
        const cardCenterX = rect.left + rect.width / 2;
        const cardCenterY = rect.top + rect.height / 2;
        
        // Calculate distance
        const distX = (x - cardCenterX) / 25; // Adjust divisor for effect intensity
        const distY = (y - cardCenterY) / 25;
        
        // Only apply effect if mouse is relatively close to card
        const distance = Math.sqrt(Math.pow(x - cardCenterX, 2) + Math.pow(y - cardCenterY, 2));
        
        if (distance < 400) { // Adjust for activation distance
          card.style.transform = `perspective(1000px) rotateX(${-distY * 0.2}deg) rotateY(${distX * 0.2}deg) translateZ(10px)`;
        } else {
          card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
        }
      });
    };
    
    window.addEventListener('mousemove', handleMouseMove);
    
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);
  
  // Add scroll-triggered animations
  useEffect(() => {
    const addFloatingAnimation = () => {
      const decorativeElements = document.querySelectorAll('.feature-icon-container, .benefit-icon-container');
      
      decorativeElements.forEach((element, index) => {
        // Create slight random variation in animation
        const delay = index * 0.2;
        const duration = 3 + Math.random();
        
        element.style.animation = `float ${duration}s ease-in-out ${delay}s infinite alternate`;
      });
    };
    
    addFloatingAnimation();
    
    // Add reveal-on-scroll class to appropriate elements
    const scrollElements = document.querySelectorAll('.feature-card, .benefit-card, .hero-content, .cta-container');
    scrollElements.forEach(element => {
      element.classList.add('reveal-on-scroll');
    });
    
    // Observer for scroll animations
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }
        });
      },
      {
        root: null,
        threshold: 0.1,
        rootMargin: '-50px'
      }
    );
    
    scrollElements.forEach(element => {
      element.style.opacity = '0';
      element.style.transform = 'translateY(20px)';
      observer.observe(element);
    });
    
    return () => {
      scrollElements.forEach(element => {
        observer.unobserve(element);
      });
    };
  }, []);

  return (
    <div className="landing-container">
      <a href="#main-content" className="skip-to-content">Skip to content</a>
      
      <motion.div 
        className="scroll-progress"
        style={{ scaleX: scrollYProgress }}
      />
      
      <div className="navbar">
        <div className="logo">
          <FontAwesomeIcon icon={faHeartPulse} className="logo-icon" />
          MindfulChat
        </div>
        <nav className="nav-links">
          <Link to="/" className="active">Home</Link>
          <Link to="/resources">Resources</Link>
          <Link to="/chat" onClick={onStartChat}>Chat</Link>
        </nav>
      </div>

      <motion.section 
        className="hero-section"
        ref={heroRef}
        id="main-content"
        style={{ y: heroY, opacity: heroOpacity }}
      >
        <motion.div 
          className="hero-content"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        >
          <div className="hero-badge">
            <span>University Student Support</span>
          </div>
          <h1>
            Your Journey to 
            <span className="gradient-text"> Mental Clarity</span>
          </h1>
          <p>A thoughtful space created by students who understand the unique challenges of university life. We're here whenever you need perspective.</p>
          <motion.div className="hero-buttons">
            <motion.button 
              className="primary-button"
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              onClick={onStartChat}
            >
              <FontAwesomeIcon icon={faComments} className="button-icon" />
              Begin Your Conversation
            </motion.button>
            <motion.button 
              className="secondary-button"
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
            >
              Explore Our Approach
              <FontAwesomeIcon icon={faArrowRight} className="button-icon" />
            </motion.button>
          </motion.div>
        </motion.div>
        <motion.div 
          className="hero-image"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.7 }}
        >
          <img 
            src={mentalWellnessSvg} 
            alt="Mental wellness illustration showing a mind garden with flowers representing growth and peace" 
          />
          <div className="floating-elements">
            <div className="floating-element" style={{ left: '10%', top: '20%' }}></div>
            <div className="floating-element" style={{ right: '15%', bottom: '25%' }}></div>
            <div className="floating-element" style={{ left: '20%', bottom: '15%' }}></div>
          </div>
        </motion.div>
      </motion.section>

      <section className="features-section" ref={featuresRef}>
        <motion.h2 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          Navigating Your Unique Challenges
        </motion.h2>
        <p className="section-subtitle">Student life presents complex, often overlapping challenges that require a nuanced understanding</p>
        <div className="features-grid">
          {[
            {
              icon: faMoneyBillWave,
              title: "Financial Navigation",
              description: "Breaking down the complex world of student finances, from uncovering hidden scholarship opportunities to creating sustainable spending patterns that reduce anxiety"
            },
            {
              icon: faGraduationCap,
              title: "Academic Balance",
              description: "Developing personalized approaches to workload management, perfectionism, and finding meaning in your studies beyond just grades and performance"
            },
            {
              icon: faPuzzlePiece,
              title: "Authentic Connection",
              description: "Moving beyond superficial interactions to build meaningful relationships that combat the increasingly documented phenomenon of campus loneliness"
            },
            {
              icon: faMountain,
              title: "Emotional Resilience",
              description: "Building adaptive coping mechanisms tailored to your personal experience, creating sustainable practices that evolve with your journey"
            }
          ].map((feature, index) => (
            <motion.div 
              key={index}
              className="feature-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="feature-icon-container">
                <FontAwesomeIcon icon={feature.icon} className="feature-icon" />
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="benefits-section" ref={benefitsRef}>
        <div className="benefits-content">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            Our Thoughtful Approach
          </motion.h2>
          <p className="section-subtitle">Beyond just quick fixes, we've designed an experience that respects the complexity of your mental landscape</p>
          <div className="benefits-grid">
            {[
              {
                icon: faCompass,
                title: "Context-Aware Guidance",
                description: "Responses that understand the specific realities of university environments, not generic advice from chatbots"
              },
              {
                icon: faShieldHeart,
                title: "Safety Through Design",
                description: "Built with student privacy as a foundational principle, not as an afterthought"
              },
              {
                icon: faHandHoldingHeart,
                title: "Judgment-Free Zone",
                description: "A space where your thoughts are met with understanding rather than evaluation or assessment"
              },
              {
                icon: faRocket,
                title: "Gateway to Resources",
                description: "Connecting you to specialized campus resources when conversations need to transition to in-person support"
              }
            ].map((benefit, index) => (
              <motion.div
                key={index}
                className="benefit-card"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="benefit-icon-container">
                  <FontAwesomeIcon icon={benefit.icon} className="benefit-icon" />
                </div>
                <div className="benefit-content">
                  <h3>{benefit.title}</h3>
                  <p>{benefit.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="cta-section" ref={ctaRef}>
        <motion.div
          className="cta-container"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2>Take the first step in your mental clarity journey</h2>
          <p>Start a conversation that acknowledges the full complexity of what you're going through—no simplistic answers, just thoughtful guidance.</p>
          <motion.button
            className="primary-button cta-button"
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={onStartChat}
          >
            <FontAwesomeIcon icon={faComments} className="button-icon" />
            Begin Your Conversation
          </motion.button>
        </motion.div>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <div className="footer-logo">
            <FontAwesomeIcon icon={faHeartPulse} className="logo-icon" />
            MindfulChat
          </div>
          <p className="footer-copyright">© {new Date().getFullYear()} MindfulChat. All rights reserved.</p>
          <p className="footer-disclaimer">MindfulChat is not a replacement for professional mental health services.</p>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage; 