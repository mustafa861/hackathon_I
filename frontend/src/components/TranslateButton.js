import React, { useState } from 'react';
import { useSkills } from '../hooks/useSkills';
import { useAuth } from '../hooks/useAuth';

export function TranslateButton({ chapterSlug, originalContent, onContentChange }) {
  const { isAuthenticated } = useAuth();
  const { translateChapter, loading } = useSkills();
  const [isTranslated, setIsTranslated] = useState(false);

  const handleClick = async () => {
    if (isTranslated) {
      onContentChange(originalContent);
      setIsTranslated(false);
    } else {
      try {
        // Try to call the translation function without authentication
        // The useSkills hook will handle the API call
        const translated = await translateChapter(chapterSlug, originalContent);
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