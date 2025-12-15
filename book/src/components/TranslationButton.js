import React, { useState, useEffect, useRef } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import './TranslationButton.css'; // Import the CSS file for styling

const TranslationButton = ({
  content,
  chapterId = null,
  sectionId = null
}) => {
  const [isTranslated, setIsTranslated] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [originalContent, setOriginalContent] = useState(null);
  const contentContainerRef = useRef(null);
  const { colorMode } = useColorMode();
  const isDarkMode = colorMode === 'dark';

  // Check if user is authenticated by checking for token in localStorage
  const isAuthenticated = () => {
    return localStorage.getItem('access_token') !== null;
  };

  // Get the content to be translated when the component mounts
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

  const handleTranslate = async () => {
    if (!isAuthenticated()) {
      alert('Please sign in to use content translation.');
      return;
    }

    // Get the current content to send for translation
    const contentToSend = originalContent || content;
    if (!contentToSend) {
      alert('No content available for translation.');
      return;
    }

    setIsProcessing(true);

    try {
      const response = await fetch('/api/translation/translate', {  // Using relative path
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,  // Include auth token
        },
        body: JSON.stringify({
          content: contentToSend,
          target_language: 'ur',
          chapter_id: chapterId,
          section_id: sectionId
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Translation failed');
      }

      const result = await response.json();

      // Find the content container and replace its content
      const contentDiv = document.querySelector('article.markdown');
      if (contentDiv) {
        // Store original content if not already stored
        if (!originalContent) {
          setOriginalContent(contentDiv.innerHTML);
        }

        // Replace with translated content
        contentDiv.innerHTML = result.translated_content;
        setIsTranslated(true);
      }
    } catch (error) {
      console.error('Translation error:', error);
      alert(`Translation failed: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    // Restore original content
    const contentDiv = document.querySelector('article.markdown');
    if (contentDiv && originalContent) {
      contentDiv.innerHTML = originalContent;
      setIsTranslated(false);
    }
  };

  return (
    <div className={`translation-container ${isDarkMode ? 'dark-mode' : 'light-mode'}`} ref={contentContainerRef}>
      <div className="translation-controls">
        <button
          className={`translate-button ${isTranslated ? 'active' : ''}`}
          onClick={isTranslated ? handleReset : handleTranslate}
          disabled={isProcessing}
          title={isTranslated ? 'Reset to original content' : 'Translate content to Urdu'}
        >
          {isProcessing ? (
            <span className="loading">Translating...</span>
          ) : isTranslated ? (
            <span>Reset Translation</span>
          ) : (
            <span>.Translate to Urdu</span>
          )}
        </button>
      </div>
      {isTranslated && (
        <div className="translation-indicator">
          Content has been translated to Urdu
        </div>
      )}
    </div>
  );
};

export default TranslationButton;