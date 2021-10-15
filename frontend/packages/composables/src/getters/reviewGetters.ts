import { AgnosticRateCount } from '@vue-storefront/core';
import { NumerBayReviewGetters } from '../types';

type Review = any;
type ReviewItem = any;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getItems = (review: Review): ReviewItem[] => review?.data || [];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewId = (item: ReviewItem): string => `${item.nickname}_${item.created_at}_${item.rating}`;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewAuthor = (item: ReviewItem): string => item.reviewer?.username || 'Anonymous';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewMessage = (item: ReviewItem): string => item.text;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewRating = (item: ReviewItem): number => Number.parseInt(item.rating, 10) || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewIsVerifiedOrder = (item: ReviewItem): boolean => item?.is_verified_order;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewDate = (item: ReviewItem): string => new Date(Date.parse(item.created_at)).toLocaleString();

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getTotalReviews = (review: Review): number => review?.total || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getAverageRating = (review: Review): number => (review?.data?.reduce((
  acc, curr
) => Number.parseInt(`${acc}`, 10) + getReviewRating(curr), 0)) / (review?.total || 1) || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getRatesCount = (review: Review): AgnosticRateCount[] => [];

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewsPage = (review: Review): number => review?.reviews.page_info?.page_size || 0;

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getReviewMetadata = (reviewData: any[]): any[] => reviewData?.map((m) => ({
  ...m,
  values: m.values.map((v) => ({
    label: (Number.parseInt(v.value, 10) || v.value),
    id: v.value_id
  }))
}));

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const getProductName = (review: any): string => review?.product?.name || '';

const reviewGetters: NumerBayReviewGetters = {
  getItems,
  getReviewId,
  getReviewAuthor,
  getReviewMessage,
  getReviewRating,
  getReviewIsVerifiedOrder,
  getReviewDate,
  getTotalReviews,
  getAverageRating,
  getRatesCount,
  getReviewsPage,
  getReviewMetadata,
  getProductName
};

export default reviewGetters;
