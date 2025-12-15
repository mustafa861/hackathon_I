import React, { useState, useEffect, useRef } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import './PersonalizationButton.css'; // Import the CSS file for styling

const PersonalizationButton = ({
  content,
  chapterId = null,
  sectionId = null
}) => {
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [originalContent, setOriginalContent] = useState(null);
  const contentContainerRef = useRef(null);
  const { colorMode } = useColorMode();
  const isDarkMode = colorMode === 'dark';

  // Check if user is authenticated by checking for token in localStorage
  const isAuthenticated = () => {
    return localStorage.getItem('access_token') !== null;
  };

  // Get the content to be personalized when the component mounts
  useEffect(() => {
    // Try to get content from props first, otherwise find it in the DOM
    if (content) {
      setOriginalContent(content);
    } else {
      // Find the closest content container
      const parentArticle = document.querySelector('article.markdown');
      if (parentArticle) {
        setOriginalContent(parentArticle.innerHTML);
      }
    }
  }, [content]);

  const handlePersonalize = async () => {
    if (!isAuthenticated()) {
      alert('Please sign in to use content personalization.');
      return;
    }

    // Get the current content to send for personalization
    const contentToSend = originalContent || content;
    if (!contentToSend) {
      alert('No content available for personalization.');
      return;
    }

    setIsProcessing(true);

    try {
      const response = await fetch('/api/personalization/personalize', {  // Using relative path
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,  // Include auth token
        },
        body: JSON.stringify({
          content: contentToSend,
          chapter_id: chapterId,
          section_id: sectionId
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Personalization failed');
      }

      const result = await response.json();

      // Find the content container and replace its content
      const contentDiv = document.querySelector('article.markdown');
      if (contentDiv) {
        // Store original content if not already stored
        if (!originalContent) {
          setOriginalContent(contentDiv.innerHTML);
        }

        // Replace with personalized content
        contentDiv.innerHTML = result.personalized_content;
        setIsPersonalized(true);
      }
    } catch (error) {
      console.error('Personalization error:', error);
      alert(`Personalization failed: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    // Restore original content
    const contentDiv = document.querySelector('article.markdown');
    if (contentDiv && originalContent) {
      contentDiv.innerHTML = originalContent;
      setIsPersonalized(false);
    }
  };

  return (
    <div className={`personalization-container ${isDarkMode ? 'dark-mode' : 'light-mode'}`} ref={contentContainerRef}>
      <div className="personalization-controls">
        <button
          className={`personalize-button ${isPersonalized ? 'active' : ''}`}
          onClick={isPersonalized ? handleReset : handlePersonalize}
          disabled={isProcessing}
          title={isPersonalized ? 'Reset to original content' : 'Personalize content based on your profile'}
        >
          {isProcessing ? (
            <span className="loading">Processing...</span>
          ) : isPersonalized ? (
            <span>Reset Content</span>
          ) : (
            <span>Personalize Content</span>
          )}
        </button>
      </div>
      {isPersonalized && (
        <div className="personalization-indicator">
          Content has been personalized based on your profile
        </div>
      )}
    </div>
  );
};

export default PersonalizationButton;