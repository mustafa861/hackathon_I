import { useState } from 'react';
import { useAuth } from './useAuth';

export function useSkills() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);

  const personalizeChapter = async (chapterSlug, content) => {
    if (!user) throw new Error('Not authenticated');

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/personalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`,
        },
        body: JSON.stringify({ chapter_slug: chapterSlug, content }),
      });

      if (!response.ok) throw new Error('Personalization failed');

      const data = await response.json();
      return data.personalized_content;
    } finally {
      setLoading(false);
    }
  };

  const translateChapter = async (chapterSlug, content) => {
    if (!user) throw new Error('Not authenticated');

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`,
        },
        body: JSON.stringify({ chapter_slug: chapterSlug, content }),
      });

      if (!response.ok) throw new Error('Translation failed');

      const data = await response.json();
      return data.translated_content;
    } finally {
      setLoading(false);
    }
  };

  return { personalizeChapter, translateChapter, loading };
}