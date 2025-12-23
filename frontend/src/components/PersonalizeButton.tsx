import React, { useState } from 'react';
import { useSkills } from '../hooks/useSkills';
import { useAuth } from '../hooks/useAuth';

interface Props {
  chapterSlug: string;
  originalContent: string;
  onContentChange: (newContent: string) => void;
}

export function PersonalizeButton({ chapterSlug, originalContent, onContentChange }: Props) {
  const { isAuthenticated } = useAuth();
  const { personalizeChapter, loading } = useSkills();
  const [isPersonalized, setIsPersonalized] = useState(false);

  if (!isAuthenticated) return null;  // Hide button for guests

  const handleClick = async () => {
    if (isPersonalized) {
      // Restore original
      onContentChange(originalContent);
      setIsPersonalized(false);
    } else {
      // Personalize
      try {
        const personalized = await personalizeChapter(chapterSlug, originalContent);
        onContentChange(personalized);
        setIsPersonalized(true);
      } catch (error) {
        console.error('Personalization error:', error);
        alert('Failed to personalize content');
      }
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className={loading ? "personalize-btn" : "personalize-btn"}
      style={{
        padding: '10px 20px',
        backgroundColor: isPersonalized ? '#888' : '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: loading ? 'wait' : 'pointer',
        marginRight: '10px',
      }}
    >
      {loading ? 'Personalizing...' : isPersonalized ? 'Show Original' : 'Personalize'}
    </button>
  );
}