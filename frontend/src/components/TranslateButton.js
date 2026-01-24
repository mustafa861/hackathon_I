import React, { useState } from 'react';
import { useSkills } from '../hooks/useSkills';

export function TranslateButton({ chapterSlug, originalContent, onContentChange }) {
  const { translateChapter, loading } = useSkills();
  const [isTranslated, setIsTranslated] = useState(false);

  const handleClick = async () => {
    // Get content dynamically if not provided initially
    const contentToUse = originalContent || (() => {
      const articleElement = document.querySelector('article.markdown');
      return articleElement?.innerText || articleElement?.textContent || '';
    })();

    if (isTranslated) {
      onContentChange(contentToUse);
      setIsTranslated(false);
    } else {
      try {
        // Try to call the translation function without authentication
        // The useSkills hook will handle the API call
        const translated = await translateChapter(chapterSlug, contentToUse);
        onContentChange(translated);
        setIsTranslated(true);
      } catch (error) {
        console.error('Translation error:', error);
        // Show more specific error message
        alert(`Could not translate content at this time: ${error.message}`);
      }
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className="translate-btn"
    >
      {loading ? 'Translating...' : isTranslated ? 'Show English' : 'Read in Urdu'}
    </button>
  );
}