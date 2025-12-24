import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

// Import the images from static/img directory
import Image1 from '@site/static/img/download(4).jpg';
import Image2 from '@site/static/img/download (1).jpg';
import Image3 from '@site/static/img/download.jpg';

const FeatureList = [
  {
    title: 'Physical AI',
    image: Image1,
    description: (
      <>
        Learn about AI that interacts with the physical world, combining robotics and intelligence.
      </>
    ),
  },
  {
    title: 'AI Concepts',
    image: Image2,
    description: (
      <>
        Explore AI concepts and how they apply to robotics and intelligent systems.
      </>
    ),
  },
  {
    title: 'AI Robots',
    image: Image3,
    description: (
      <>
        Discover how AI powers robotic systems for autonomous decision making.
      </>
    ),
  },
];

function Feature({image, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img src={image} className={styles.featureImage} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}