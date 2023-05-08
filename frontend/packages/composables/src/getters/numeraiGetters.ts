/* istanbul ignore file */
import moment from 'moment';
import { Numerai, NumeraiGetters } from '../types';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getCorrRank = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestRanks?.corr;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getMmcRank = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestRanks?.mmc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFncRank = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestRanks?.fnc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getTcRank = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestRanks?.tc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getCorrRep = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReps?.corr;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getMmcRep = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReps?.mmc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getFncRep = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReps?.fnc;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getTcRep = (numerai: any): number => numerai?.modelInfo?.modelPerformance?.latestReps?.tc;

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

export const getRoundModelPerformancesTableData = (numerai: any) => {
  return numerai.filter(o=>(Boolean(o?.submissionScores)));
}

export const extractNumeraiV2Scores = (numerai: any, scoreName: string, isPercentile: boolean) => {
  const scores = numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => ({x: moment.utc(o?.roundDataDatestamp, "YYYYMMDD").format('YYYY-MM-DD'), y: o?.submissionScores}))
  const extractedScores = (scores || []).map(roundScores => ({x: roundScores.x, y: roundScores.y.filter(score => score?.displayName === scoreName)[0]}))
  if (isPercentile) {
    return extractedScores?.map(o=> ({x: o.x, y: o.y?.percentile})).filter(o=>Boolean(o.y))
  }
  return extractedScores?.map(o=> ({x: o.x, y: o.y?.value})).filter(o=>Boolean(o.y))
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getNumeraiCorrCorr60TcChartData = (numerai_raw: any) => {
  const numerai = numerai_raw.filter(o => moment.utc(o?.roundDataDatestamp, "YYYYMMDD") >= moment().subtract(1, 'years'))
  return {
    labels: numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => moment.utc(o?.roundDataDatestamp, "YYYYMMDD").format('YYYY-MM-DD')),
    datasets: [
      {
        label: 'CORR',
        borderColor: '#666666',
        fill: false,
        lineTension: 0,
        borderWidth: 2,
        pointRadius: 0,
        data: extractNumeraiV2Scores(numerai, 'corr20', false),
        data1: extractNumeraiV2Scores(numerai, 'corr20', true).map(o=>o?.y),
        data2: numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => o?.roundNumber)
      },
      {
        label: 'TC',
        borderColor: '#a278dc',
        fill: false,
        lineTension: 0,
        borderWidth: 2,
        pointRadius: 0,
        data: extractNumeraiV2Scores(numerai, 'tc', false),
        data1: extractNumeraiV2Scores(numerai, 'tc', true).map(o=>o?.y),
        data2: numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => o?.roundNumber)
      }
    ]
  };
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getSignalsCorrChartData = (numerai_raw: any) => {
  const numerai = numerai_raw.filter(o => moment.utc(o?.roundDataDatestamp, "YYYYMMDD") >= moment().subtract(1, 'years'))
  return {
    labels: numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => moment.utc(o?.roundDataDatestamp, "YYYYMMDD").format('YYYY-MM-DD')),
    datasets: [
      {
        label: 'CORR',
        borderColor: '#666666',
        fill: false,
        lineTension: 0,
        borderWidth: 2,
        pointRadius: 0,
        data: extractNumeraiV2Scores(numerai, 'corr', false),
        data1: extractNumeraiV2Scores(numerai, 'corr', true).map(o=>o?.y),
        data2: numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => o?.roundNumber)
      },
    ]
  };
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getSignalsTcIcChartData = (numerai_raw: any) => {
  const numerai = numerai_raw.filter(o => moment.utc(o?.roundDataDatestamp, "YYYYMMDD") >= moment().subtract(1, 'years'))
  return {
    labels: numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => moment.utc(o?.roundDataDatestamp, "YYYYMMDD").format('YYYY-MM-DD')),
    datasets: [
      {
        label: 'TC',
        borderColor: '#a278dc',
        fill: false,
        lineTension: 0,
        borderWidth: 2,
        pointRadius: 0,
        data: extractNumeraiV2Scores(numerai, 'tc', false),
        data1: extractNumeraiV2Scores(numerai, 'tc', true).map(o=>o?.y),
        data2: numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => o?.roundNumber)
      },
      {
        label: 'IC',
        borderColor: '#acacac',
        fill: false,
        lineTension: 0,
        borderWidth: 2,
        pointRadius: 0,
        data: extractNumeraiV2Scores(numerai, 'ic', false),
        data1: extractNumeraiV2Scores(numerai, 'ic', true).map(o=>o?.y),
        data2: numerai.filter(o => Boolean(o?.submissionScores)).slice().reverse().map(o => o?.roundNumber)
      },
    ]
  };
};


const numeraiGetters: NumeraiGetters<Numerai> = {
  getCorrRank,
  getMmcRank,
  getFncRank,
  getTcRank,
  getCorrRep,
  getMmcRep,
  getFncRep,
  getTcRep,
  getMetaCorr,
  getOneDayReturn,
  getThreeMonthsReturn,
  getOneYearReturn,
  getNmrStaked,
  getWokeDateTime,
  getWokeDate,
  getFormatted,
  getNumeraiCorrCorr60TcChartData,
  getSignalsCorrChartData,
  getSignalsTcIcChartData,
  getRoundModelPerformancesTableData
};

export default numeraiGetters;
