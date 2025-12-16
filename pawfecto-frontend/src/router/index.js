import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SignupBrandView from '../views/SignupBrandView.vue'
import SignupCreatorView from '../views/SignupCreatorView.vue'
import api from "@/plugins/axios"

// Brand
import BrandDashboardLayout from '@/views/brand/BrandDashboardLayout.vue'
import BrandCampaignListView from '@/views/brand/BrandCampaignListView.vue'
import BrandCreateCampaignView from '@/views/brand/BrandCreateCampaignView.vue'
import BrandCampaignDetailView from '@/views/brand/BrandCampaignDetailView.vue'
import BrandUpdateCampaignView from '@/views/brand/BrandUpdateCampaignView.vue'

// Creator
import CreatorDashboardLayout from '@/views/creator/CreatorDashboardLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup/brand',
      name: 'signup-brand',
      component: SignupBrandView,
    },
    {
      path: '/signup/creator',
      name: 'signup-creator',
      component: SignupCreatorView,
    }, 
     /* ------------------------------------------
      BRAND DASHBOARD 구조
    ------------------------------------------ */
    {
      path: "/dashboard/brand/:brand_id",
      component: BrandDashboardLayout,   // 레이아웃 역할
      props: true,
      children: [
        {
          path: "",
          redirect: to => `/dashboard/brand/${to.params.brand_id}/campaign-list`
        },
        {
          path: 'campaign-list',
          name: 'brand-campaign-list',
          props: true,
          component: BrandCampaignListView
        },
        {
          path: "create-campaign",
          name: "brand-create-campaign",
          component: BrandCreateCampaignView,
          props: true,
        },
        {
          path: "campaign/:campaign_id/update",
          name: "brand-update-campaign",
          component: BrandUpdateCampaignView,
          props: true
        },
        {
          path: "campaign/:campaign_id",
          name: "brand-campaign-detail",
          component: BrandCampaignDetailView,
          props: true,
          children: [
            {
              path: "",
              redirect: to => `/dashboard/brand/${to.params.brand_id}/campaign/${to.params.campaign_id}/recommendations`
            },
            {
              path: "recommendations",
              name: "campaign-recommendations",
              component: () =>
                import(
                  "@/components/brand/BrandCampaignRecommendationsTable.vue"
                ),
              props: true,
            },
            {
              path: "status",
              name: "campaign-status",
              component: () =>
                import("@/components/brand/BrandCampaignStatusTable.vue"),
              props: true,
            },
          ],
        },
        {
          path: 'brand-settings',
          name: 'brand-settings',
          component: () =>
            import('@/views/brand/BrandSettingsView.vue'),
          props: true
        },
        {
          path: 'brand-settings-update',
          name: 'brand-settings-update',
          component: () =>
            import('@/views/brand/BrandUpdateSettingsView.vue'),
          props: true
        }
      ],
    },
     /* ------------------------------------------
      CREATOR DASHBOARD 구조
    ------------------------------------------ */
    {
      path: '/dashboard/creator/:creator_id',
      component: CreatorDashboardLayout,   // 레이아웃 역할
      props: true,
      children: [
        {
          path: '',
          redirect: to => `/dashboard/creator/${to.params.creator_id}/campaign-offers`
        },
        {
          path: 'campaign-offers',
          name: 'creator-campaign-offers',
          props: route => ({ creatorId: Number(route.params.creator_id) }),
          component: () =>
                import(
                  "@/components/creator/CreatorCampaignOffersTable.vue"
                ),
        },
        {
          path: 'campaign-progress',
          name: 'creator-campaign-progress',
          props: route => ({ creatorId: Number(route.params.creator_id) }),
          component: () =>
                import(
                  "@/components/creator/CreatorCampaignProgressTable.vue"
                ),
        },
        {
          path: 'creator-settings',
          name: 'creator-settings',
          component: () =>
            import('@/views/creator/CreatorSettingsView.vue'),
          props: route => ({
            creatorId: Number(route.params.creator_id)
          })
        },
        {
          path: 'creator-settings-update',
          name: 'creator-settings-update',
          component: () =>
            import('@/views/creator/CreatorUpdateSettingsView.vue'),
          props: route => ({
            creatorId: Number(route.params.creator_id)
          })
        }
      ]
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  // dashboard 경로만 검사
  if (!to.path.startsWith('/dashboard')) {
    return next()
  }

  try {
    const res = await api.get('/accounts/me/')
    const accountType = res.data.account_type

    if (
      to.path.startsWith('/dashboard/brand') &&
      accountType !== 'brand'
    ) {
      return next('/login')
    }

    if (
      to.path.startsWith('/dashboard/creator') &&
      accountType !== 'creator'
    ) {
      return next('/login')
    }

    next()
  } catch (err) {
    next('/login')
  }
})


export default router
