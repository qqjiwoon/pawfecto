import { defineStore } from 'pinia';
import api from '@/plugins/axios'; // API 요청을 위한 axios 임포트
import { useWarningStore } from './warning'; // 경고 메시지 관리용 store

export const useCreatorStore = defineStore('creator', {
  state: () => ({
    creators: [], // 기존 크리에이터 목록
    recommendedCreators: [], // 추천된 크리에이터 목록
    loading: false, // 로딩 상태
  }),
  actions: {
    // 크리에이터 추천 API 호출
    async recommendCreators(campaignId, brandId) {
      const warningStore = useWarningStore();
      try {
        this.loading = true; // 로딩 시작

        // 서버로 추천 크리에이터 API 요청
        const response = await api.post(`/api/v1/brand/${brandId}/campaign/${campaignId}/auto-match/`);

        // 추천된 크리에이터 리스트를 저장
        this.recommendedCreators = response.data.map(creator => ({
          id: creator.campaign_acceptance_id,
          name: creator.creator.name,
          handle: creator.creator.sns_handle || creator.creator.username,
          profileImg: creator.creator.profile_image_url,
          petType: creator.creator.pet_type,
          followers: creator.creator.follower_count ?? 0,
          styleTags: creator.creator.style_tags || [],
          brandStatus: creator.brand_decision_status,
          creatorStatus: creator.acceptance_status,
        }));

        warningStore.open('크리에이터 추천이 완료되었습니다!');
      } catch (error) {
        console.error(error);
        warningStore.open('추천 과정에서 오류가 발생했습니다.');
      } finally {
        this.loading = false; // 로딩 종료
      }
    },

    // 추천 크리에이터 목록 추가
    addRecommendedCreators(newCreators) {
      this.recommendedCreators = [...this.recommendedCreators, ...newCreators];
    },
  },
});
