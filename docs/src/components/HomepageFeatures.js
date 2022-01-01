import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Direct Buy and Sell',
    Svg: require('../../static/img/Circle-icons-computer.svg').default,
    description: (
      <>
        NumerBay is a marketplace for the Numerai Community. Anything related to the Numerai tournaments can be traded directly without middleman.
      </>
    ),
  },
  {
    title: 'Automated Submission',
    Svg: require('../../static/img/Circle-icons-gear.svg').default,
    description: (
      <>
        NumerBay offers automated submission for buyers. Non-tournament participants can stake on others' predictions by buying on NumerBay and setting up auto-submission.
      </>
    ),
  },
  {
    title: 'Community Owned',
    Svg: require('../../static/img/Circle-icons-dev.svg').default,
    description: (
      <>
        NumerBay is sponsored by the Numerai Council of Elders and developed by the Numerai Community.
      </>
    ),
  }
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
