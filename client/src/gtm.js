import TagManager from 'react-gtm-module';

export const initGTM = (gtmId) => {
  if (gtmId) {
    TagManager.initialize({ gtmId });
  } else {
    console.error('GTM ID is not defined in the environment variables.');
  }
};
