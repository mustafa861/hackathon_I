import React, { useState } from 'react';
import { useSkills } from '../hooks/useSkills';
import { useAuth } from '../hooks/useAuth';

export function PersonalizeButton({ chapterSlug, originalContent, onContentChange }) {
  const { isAuthenticated } = useAuth();
  const { personalizeChapter, loading } = useSkills();
  const [isPersonalized, setIsPersonalized] = useState(false);

  const handleClick = async () => {
    if (isPersonalized) {
      // Restore original
      onContentChange(originalContent);
      setIsPersonalized(false);
    } else {
      // Personalize - try without authentication first
      try {
        // Try to call the personalization function without authentication
        // The useSkills hook will handle the API call
        const personalized = await personalizeChapter(chapterSlug, originalContent);
        onContentChange(personalized);
        setIsPersonalized(true);
      } catch (error) {
        console.error('Personalization error:', error);
        // If it fails, we can still show an error but not require login
        alert('Could not personalize content at this time');
      }
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className={loading ? "translate-btn" : "personalize-btn"}
    >
      {loading ? 'Personalizing...' : isPersonalized ? 'Show Original' : 'Personalize'}
    </button>
  );
}