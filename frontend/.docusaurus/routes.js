import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', 'f84'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '7eb'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', '4b3'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', '596'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '4d4'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '538'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '21f'),
    exact: true
  },
  {
    path: '/login',
    component: ComponentCreator('/login', 'cff'),
    exact: true
  },
  {
    path: '/login',
    component: ComponentCreator('/login', '9ad'),
    exact: true
  },
  {
    path: '/signup',
    component: ComponentCreator('/signup', '6ab'),
    exact: true
  },
  {
    path: '/signup',
    component: ComponentCreator('/signup', '20b'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'e55'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '59b'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'f99'),
            routes: [
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'a16'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/intro_with_quiz',
                component: ComponentCreator('/docs/intro_with_quiz', '2dc'),
                exact: true
              },
              {
                path: '/docs/ros2-nodes',
                component: ComponentCreator('/docs/ros2-nodes', '12c'),
                exact: true,
                sidebar: "docs"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'abd'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
