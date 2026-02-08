// import { useState } from 'react';
// import { useAuth } from './useAuth';
// import { API_BASE_URL } from '../constants/api';

// export function useSkills() {
//   const { user } = useAuth();
//   const [loading, setLoading] = useState(false);

//   const personalizeChapter = async (chapterSlug, content) => {
//     if (!user) throw new Error('Not authenticated');

//     setLoading(true);
//     try {
//       const response = await fetch(`${API_BASE_URL}/api/personalize`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': `Bearer ${user.token}`,
//         },
//         body: JSON.stringify({ chapter_slug: chapterSlug, content }),
//       });

//       if (!response.ok) throw new Error('Personalization failed');

//       const data = await response.json();
//       return data.personalized_content;
//     } finally {
//       setLoading(false);
//     }
//   };

//   const translateChapter = async (chapterSlug, content) => {
//     if (!user) throw new Error('Not authenticated');

//     setLoading(true);
//     try {
//       const response = await fetch(`${API_BASE_URL}/api/translate`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': `Bearer ${user.token}`,
//         },
//         body: JSON.stringify({ chapter_slug: chapterSlug, content }),
//       });

//       if (!response.ok) throw new Error('Translation failed');

//       const data = await response.json();
//       return data.translated_content;
//     } finally {
//       setLoading(false);
//     }
//   };

//   return { personalizeChapter, translateChapter, loading };
// }



import { useState } from 'react';
import { useAuth } from './useAuth';
import { API_BASE_URL } from '../constants/api';

export function useSkills() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);

  const personalizeChapter = async (chapterSlug, content) => {
    if (!user) throw new Error('Not authenticated');

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/personalize`, {
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
    // ✅ REMOVED authentication check - translation works for everyone
    
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // ✅ REMOVED Authorization header
        },
        body: JSON.stringify({ chapter_slug: chapterSlug, content }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Translation failed');
      }

      const data = await response.json();
      return data.translated_content;
    } catch (error) {
      console.error('Translation error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { personalizeChapter, translateChapter, loading };
}