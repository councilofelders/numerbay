import { PollGetters } from '../types';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getPollTopic = (poll: any): string => poll?.topic || '-';

export const getPollDescription = (poll: any): any => (poll as any)?.description || '';

export const getPollEndDate = (poll: any): any => (poll as any)?.date_finish ? new Date(Date.parse((poll as any)?.date_finish)).toLocaleString() : '-';

export const getPollId = (poll: any): string => (poll as any)?.id || '';

export const getPollOptions = (poll: any): any[] => (poll as any)?.options || [];

export const getPollOrderedOptions = (poll: any): any[] => (poll as any)?.options ? (poll as any)?.options.slice().sort((a, b) => parseFloat(a.id) - parseFloat(b.id)) : [];

export const getPollOptionById = (poll: any, optionId: number): any => {
  const options = (poll as any)?.options?.filter((o)=>parseInt(o.id) === parseInt(String(optionId))) || [];
  return options[0] || {};
};

export const getPollOrderedOption = (poll: any, optionIdx = 0): any => {
  const orderedOptions = getPollOrderedOptions(poll);
  return orderedOptions[parseInt(String(optionIdx))] || {};
};

export const getPollWeightMode = (poll: any): string => (poll as any)?.weight_mode;

export const getPollStakeLimit = (poll: any): string => (poll as any)?.stake_limit ? `${(poll as any)?.stake_limit} NMR` : '-';

export const getPollIsActive = (poll: any): boolean => (poll as any)?.date_finish ? (Date.parse((poll as any)?.date_finish) > Date.now()) : false;

export const getPollExpirationRound = (poll: any): number => (poll as any)?.expiration_round || null;

export const getPollOwner = (poll: any): string => (poll as any)?.owner?.username || '-';

const pollGetters: PollGetters<any> = {
  getTopic: getPollTopic,
  getDescription: getPollDescription,
  getEndDate: getPollEndDate,
  getId: getPollId,
  getOptionById: getPollOptionById,
  getOrderedOption: getPollOrderedOption,
  getOptions: getPollOptions,
  getOrderedOptions: getPollOrderedOptions,
  getWeightMode: getPollWeightMode,
  getStakeLimit: getPollStakeLimit,
  getIsActive: getPollIsActive,
  getExpirationRound: getPollExpirationRound,
  getOwner: getPollOwner
};

export default pollGetters;
