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
    path: '/signup',
    component: ComponentCreator('/signup', '6ab'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '072'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'd15'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '2ac'),
            routes: [
              {
                path: '/docs/ch1_1_introduction_to_physical_ai',
                component: ComponentCreator('/docs/ch1_1_introduction_to_physical_ai', 'e15'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/ch1_2_sensing_and_perception',
                component: ComponentCreator('/docs/ch1_2_sensing_and_perception', '807'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/ch1_3_actuation_and_control',
                component: ComponentCreator('/docs/ch1_3_actuation_and_control', 'efd'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/ch2_1_humanoid_robot_design',
                component: ComponentCreator('/docs/ch2_1_humanoid_robot_design', '682'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/ch2_2_locomotion_and_balance',
                component: ComponentCreator('/docs/ch2_2_locomotion_and_balance', '0be'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/ch2_3_human_robot_interaction',
                component: ComponentCreator('/docs/ch2_3_human_robot_interaction', '5b9'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/ch3_1_industrial_applications',
                component: ComponentCreator('/docs/ch3_1_industrial_applications', '6fd'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/ch3_2_service_robotics',
                component: ComponentCreator('/docs/ch3_2_service_robotics', '336'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/ch3_3_future_directions',
                component: ComponentCreator('/docs/ch3_3_future_directions', 'b70'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'a16'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/part1_fundamentals',
                component: ComponentCreator('/docs/part1_fundamentals', '96d'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/part2_humanoid_robots',
                component: ComponentCreator('/docs/part2_humanoid_robots', '4d7'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/part3_advanced_applications',
                component: ComponentCreator('/docs/part3_advanced_applications', '8f2'),
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
