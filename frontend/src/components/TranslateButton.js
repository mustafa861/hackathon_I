// import React, { useState } from 'react';
// import { useSkills } from '../hooks/useSkills';

// export function TranslateButton({ chapterSlug, originalContent, onContentChange }) {
//   const { translateChapter, loading } = useSkills();
//   const [isTranslated, setIsTranslated] = useState(false);

//   const handleClick = async () => {
//     // Get content dynamically if not provided initially
//     const contentToUse = originalContent || (() => {
//       const articleElement = document.querySelector('article.markdown');
//       return articleElement?.innerText || articleElement?.textContent || '';
//     })();

//     if (isTranslated) {
//       onContentChange(contentToUse);
//       setIsTranslated(false);
//     } else {
//       try {
//         // Try to call the translation function without authentication
//         // The useSkills hook will handle the API call
//         const translated = await translateChapter(chapterSlug, contentToUse);
//         onContentChange(translated);
//         setIsTranslated(true);
//       } catch (error) {
//         console.error('Translation error:', error);
//         // Show more specific error message
//         alert(`Could not translate content at this time: ${error.message}`);
//       }
//     }
//   };

//   return (
//     <button
//       onClick={handleClick}
//       disabled={loading}
//       className="translate-btn"
//     >
//       {loading ? 'Translating...' : isTranslated ? 'Show English' : 'Read in Urdu'}
//     </button>
//   );
// }


import React, { useState } from 'react';
import { useSkills } from '../hooks/useSkills';

export function TranslateButton({ chapterSlug, originalContent, onContentChange }) {
  const { translateChapter, loading } = useSkills();
  const [isTranslated, setIsTranslated] = useState(false);

  const handleClick = async () => {
    // Pehle originalContent check karo
    let contentToUse = originalContent;
    
    // Agar originalContent nahi hai, to page se extract karo
    if (!contentToUse || contentToUse.trim() === '') {
      const articleElement = document.querySelector('article.markdown');
      if (articleElement) {
        contentToUse = articleElement.innerText || articleElement.textContent || '';
      }
      
      // Agar phir bhi nahi mila, aur jagah try karo
      if (!contentToUse || contentToUse.trim() === '') {
        const mainContent = document.querySelector('main') || 
                           document.querySelector('.markdown-body') ||
                           document.querySelector('article');
        if (mainContent) {
          contentToUse = mainContent.innerText || mainContent.textContent || '';
        }
      }
    }

    // ✅ DEBUGGING: Console mein dekho kya bhej rahe hain
    console.log('Chapter Slug:', chapterSlug);
    console.log('Content ki length:', contentToUse?.length);
    console.log('Content ka preview:', contentToUse?.substring(0, 200));

    // ✅ Check karo ke content hai ya nahi
    if (!contentToUse || contentToUse.trim() === '') {
      alert('Translate karne ke liye koi content nahi mila. Page pura load hone ka intezar karein.');
      return;
    }

    if (isTranslated) {
      onContentChange(contentToUse);
      setIsTranslated(false);
    } else {
      try {
        const translated = await translateChapter(chapterSlug, contentToUse);
        
        // ✅ DEBUGGING: Translation ka result dekho
        console.log('Translation result:', translated);
        
        onContentChange(translated);
        setIsTranslated(true);
      } catch (error) {
        console.error('Translation error:', error);
        alert(`Translation nahi ho saka: ${error.message}`);
      }
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className="translate-btn"
    >
      {loading ? 'Translating' : isTranslated ? 'Show English' : 'Read in Urdu'}
    </button>
  );
}