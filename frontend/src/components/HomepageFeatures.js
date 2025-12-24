import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

// Import SVG images
import PhysicalAISvg from '@site/static/img/undraw_physical_ai.svg';
import AIRobotsSvg from '@site/static/img/undraw_ai_robots.svg';
import AIConceptsSvg from '@site/static/img/undraw_ai_concepts.svg';

const FeatureList = [
  {
    title: 'Physical AI',
    Svg: PhysicalAISvg,
    description: (
      <>
        Learn about AI that interacts with the physical world, combining robotics and intelligence.
      </>
    ),
  },
  {
    title: 'AI Robots',
    Svg: AIRobotsSvg,
    description: (
      <>
        Explore how artificial intelligence powers robotic systems for autonomous decision making.
      </>
    ),
  },
  {
    title: 'AI Concepts',
    Svg: AIConceptsSvg,
    description: (
      <>
        Master AI fundamentals with practical examples and interactive learning experiences.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} alt={title} />
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