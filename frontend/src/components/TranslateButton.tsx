import React, { useState } from 'react';
import { useSkills } from '../hooks/useSkills';
import { useAuth } from '../hooks/useAuth';

interface Props {
  chapterSlug: string;
  originalContent: string;
  onContentChange: (newContent: string) => void;
}

export function TranslateButton({ chapterSlug, originalContent, onContentChange }: Props) {
  const { isAuthenticated } = useAuth();
  const { translateChapter, loading } = useSkills();
  const [isTranslated, setIsTranslated] = useState(false);

  if (!isAuthenticated) return null;

  const handleClick = async () => {
    if (isTranslated) {
      onContentChange(originalContent);
      setIsTranslated(false);
    } else {
      try {
        const translated = await translateChapter(chapterSlug, originalContent);
        onContentChange(translated);
        setIsTranslated(true);
      } catch (error) {
        console.error('Translation error:', error);
        alert('Failed to translate content');
      }
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      style={{
        padding: '10px 20px',
        backgroundColor: isTranslated ? '#888' : '#28a745',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: loading ? 'wait' : 'pointer',
      }}
    >
      {loading ? 'Translating...' : isTranslated ? 'Show English' : 'Read in Urdu'}
    </button>
  );
}