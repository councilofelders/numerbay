import { AgnosticRateCount } from '@vue-storefront/core';
import { NumerBayReviewGetters } from '../types';

type Review = any;
type ReviewItem = any;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItems = (review: Review): ReviewItem[] => [];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewId = (item: ReviewItem): string => '';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewAuthor = (item: ReviewItem): string => '';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewMessage = (item: ReviewItem): string => '';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewRating = (item: ReviewItem): number => 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewDate = (item: ReviewItem): string => '';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getTotalReviews = (review: Review): number => 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getAverageRating = (review: Review): number => 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getRatesCount = (review: Review): AgnosticRateCount[] => [];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewsPage = (review: Review): number => 1;

export const getReviewMetadata = (reviewData: any[]): any[] => reviewData?.map((m) => ({
  ...m,
  values: m.values.map((v) => ({
    label: (Number.parseInt(v.value, 10) || v.value),
    id: v.value_id
  }))
}));

export const getProductName = (review: any): string => review?.product?.name || '';

const reviewGetters: NumerBayReviewGetters = {
  getItems,
  getReviewId,
  getReviewAuthor,
  getReviewMessage,
  getReviewRating,
  getReviewDate,
  getTotalReviews,
  getAverageRating,
  getRatesCount,
  getReviewsPage,
  getReviewMetadata,
  getProductName
};

export default reviewGetters;
