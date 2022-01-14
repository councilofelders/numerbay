/* istanbul ignore file */

import { Numerai, NumeraiGetters } from '../types';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getCorrRank = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestRanks?.corr;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getMmcRank = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestRanks?.mmc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFncRank = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestRanks?.fnc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getCorrRep = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReps?.corr;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getMmcRep = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReps?.mmc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFncRep = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReps?.fnc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getMetaCorr = (numerai: any): number => {
  const roundPerformances = numerai?.modelInfo?.modelPerformance?.roundModelPerformances;
  if (!roundPerformances || roundPerformances.length === 0) {
    return null;
  }
  const latestCorr = roundPerformances[0].corr;
  const idx = latestCorr ? 0 : 1;
  if (roundPerformances.length > 1 || (roundPerformances.length === 1 && idx === 0)) {
    return roundPerformances[idx].corrWMetamodel;
  }
  return null;
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getOneDayReturn = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReturns?.oneDay;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getThreeMonthsReturn = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReturns?.threeMonths;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getOneYearReturn = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReturns?.oneYear;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getNmrStaked = (numerai: any): number => numerai?.modelInfo?.nmrStaked || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWokeDateTime = (numerai: any): string => numerai?.modelInfo?.startDate;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getWokeDate = (numerai: any): string => numerai?.modelInfo?.startDate ? numerai?.modelInfo?.startDate.split('T')[0] : '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFormatted = (value: number, decimals = 4): string => value ? Number(value).toFixed(decimals) : '-';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getNumeraiChartData = (numerai: any) => {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  const transposed = Object.assign(...Object.keys(numerai.modelInfo.modelPerformance.roundModelPerformances[0]).map(
    key => ({ [key]: numerai.modelInfo.modelPerformance.roundModelPerformances.slice(0, 20).map(o => o[key]).reverse() })
  ));

  return {
    labels: transposed.roundNumber,
    datasets: [
      {
        label: 'CORR',
        borderColor: '#666666',
        fill: false,
        lineTension: 0,
        data: transposed.corr
      },
      {
        label: 'MMC',
        borderColor: '#acacac',
        fill: false,
        lineTension: 0,
        data: transposed.mmc
      }
    ]
  };
};

const numeraiGetters: NumeraiGetters<Numerai> = {
  getCorrRank,
  getMmcRank,
  getFncRank,
  getCorrRep,
  getMmcRep,
  getFncRep,
  getMetaCorr,
  getOneDayReturn,
  getThreeMonthsReturn,
  getOneYearReturn,
  getNmrStaked,
  getWokeDateTime,
  getWokeDate,
  getFormatted,
  getNumeraiChartData
};

export default numeraiGetters;
