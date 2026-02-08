// import React, { useState, useEffect } from 'react';
// import Layout from '@theme-original/DocItem/Layout';
// import { PersonalizeButton } from '../../components/PersonalizeButton';
// import { TranslateButton } from '../../components/TranslateButton';
// import { ChatWidget } from '../../components/ChatWidget';
// import { useAuth } from '../../hooks/useAuth';

// export default function LayoutWrapper(props) {
//   const [content, setContent] = useState(null);
//   const [originalContent, setOriginalContent] = useState('');
//   const { isAuthenticated } = useAuth();

//   // Extract chapter slug
//   const chapterSlug = props.content?.metadata?.unversionedId || props.content?.metadata?.id || 'unknown';

//   const handleContentChange = (newContent) => {
//     setContent(newContent);
//   };

//   // Effect to get the original content after component mounts
//   useEffect(() => {
//     // Wait a bit for the content to be rendered, then grab it
//     const timer = setTimeout(() => {
//       const articleElement = document.querySelector('article.markdown');
//       if (articleElement) {
//         const textContent = articleElement.innerText || articleElement.textContent || '';
//         setOriginalContent(textContent);
//       } else {
//         // Fallback to metadata if no content found
//         setOriginalContent(props.content?.metadata?.title || chapterSlug || '');
//       }
//     }, 100); // Small delay to ensure content is rendered

//     return () => clearTimeout(timer);
//   }, []);

//   return (
//     <>
//       <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f9f9f9', borderRadius: '5px' }}>
//         <PersonalizeButton
//           chapterSlug={chapterSlug}
//           originalContent={originalContent}
//           onContentChange={handleContentChange}
//         />
//         <TranslateButton
//           chapterSlug={chapterSlug}
//           originalContent={originalContent}
//           onContentChange={handleContentChange}
//         />
//       </div>

//       {content ? (
//         <div
//           style={{ padding: '20px' }}
//           dangerouslySetInnerHTML={{ __html: content }}
//         />
//       ) : (
//         <Layout {...props} />
//       )}

//       <ChatWidget />
//     </>
//   );
// }

import React, { useState, useEffect } from 'react';
import Layout from '@theme-original/DocItem/Layout';
import { PersonalizeButton } from '../../components/PersonalizeButton';
import { TranslateButton } from '../../components/TranslateButton';
import { ChatWidget } from '../../components/ChatWidget';
import { useAuth } from '../../hooks/useAuth';

export default function LayoutWrapper(props) {
  const [content, setContent] = useState(null);
  const [originalContent, setOriginalContent] = useState('');
  const { isAuthenticated } = useAuth();

  // Extract chapter slug
  const chapterSlug = props.content?.metadata?.unversionedId || props.content?.metadata?.id || 'unknown';

  const handleContentChange = (newContent) => {
    setContent(newContent);
  };

  // Effect to get the original content after component mounts
  useEffect(() => {
    // ✅ INCREASED timeout to give more time for content to load
    const timer = setTimeout(() => {
      const articleElement = document.querySelector('article.markdown');
      if (articleElement) {
        const textContent = articleElement.innerText || articleElement.textContent || '';
        
        // ✅ DEBUG: Check karo content mil raha hai ya nahi
        console.log('Original Content Length:', textContent.length);
        console.log('Original Content Preview:', textContent.substring(0, 100));
        
        setOriginalContent(textContent);
      } else {
        // ✅ Try alternative selectors
        const mainContent = document.querySelector('main article') || 
                           document.querySelector('.markdown') ||
                           document.querySelector('article');
        
        if (mainContent) {
          const textContent = mainContent.innerText || mainContent.textContent || '';
          console.log('Found content from alternative selector:', textContent.length);
          setOriginalContent(textContent);
        } else {
          // Fallback to metadata if no content found
          console.warn('No content found, using fallback');
          setOriginalContent(props.content?.metadata?.description || props.content?.metadata?.title || 'No content available');
        }
      }
    }, 500); // ✅ INCREASED from 100ms to 500ms

    return () => clearTimeout(timer);
  }, [props.content]); // ✅ ADDED dependency

  return (
    <>
      <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f9f9f9', borderRadius: '5px' }}>
        <PersonalizeButton
          chapterSlug={chapterSlug}
          originalContent={originalContent}
          onContentChange={handleContentChange}
        />
        <TranslateButton
          chapterSlug={chapterSlug}
          originalContent={originalContent}
          onContentChange={handleContentChange}
        />
        
        {/* ✅ DEBUG: Show content status */}
        <small style={{ display: 'block', marginTop: '5px', color: '#666' }}>
          Content loaded: {originalContent.length > 0 ? `${originalContent.length} characters` : 'Loading...'}
        </small>
      </div>

      {content ? (
        <div
          style={{ padding: '20px' }}
          dangerouslySetInnerHTML={{ __html: content }}
        />
      ) : (
        <Layout {...props} />
      )}

      <ChatWidget />
    </>
  );
}