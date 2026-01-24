import React, { useState } from 'react';
import { useSkills } from '../hooks/useSkills';

interface Props {
  chapterSlug: string;
  originalContent: string;
  onContentChange: (newContent: string) => void;
}

export function PersonalizeButton({ chapterSlug, originalContent, onContentChange }: Props) {
  const { personalizeChapter, loading } = useSkills();
  const [isPersonalized, setIsPersonalized] = useState(false);

  const handleClick = async () => {
    // Get content dynamically if not provided initially
    const contentToUse = originalContent || (() => {
      const articleElement = document.querySelector('article.markdown');
      return articleElement?.innerText || articleElement?.textContent || '';
    })();

    if (isPersonalized) {
      // Restore original
      onContentChange(contentToUse);
      setIsPersonalized(false);
    } else {
      // Personalize
      try {
        const personalized = await personalizeChapter(chapterSlug, contentToUse);
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
      className="personalize-btn"
      style={{
        padding: '10px 20px',
        backgroundColor: isPersonalized ? '#888' : '#000000', // Changed to black
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