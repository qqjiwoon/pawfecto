import { ref } from "vue"

export const campaignAcceptances = ref([
  {
    campaign_acceptance_id: 1,
    creator_id: 1,
    campaign_id: 3,
    acceptance_status: "accepted",
    applied_at: "2025-01-05 13:20:00",
    accepted_at: "2025-01-07 09:10:00"
  },
  {
    campaign_acceptance_id: 2,
    creator_id: 2,
    campaign_id: 1,
    acceptance_status: "completed",
    applied_at: "2025-01-03 10:42:00",
    accepted_at: "2025-01-04 15:18:00"
  },
  {
    campaign_acceptance_id: 3,
    creator_id: 3,
    campaign_id: 4,
    acceptance_status: "accepted",
    applied_at: "2025-01-12 18:11:00",
    accepted_at: "2025-01-14 12:33:00"
  },
  {
    campaign_acceptance_id: 4,
    creator_id: 4,
    campaign_id: 2,
    acceptance_status: "pending",
    applied_at: "2025-01-20 09:44:00",
    accepted_at: null
  },
  {
    campaign_acceptance_id: 5,
    creator_id: 5,
    campaign_id: 5,
    acceptance_status: "completed",
    applied_at: "2025-01-10 14:29:00",
    accepted_at: "2025-01-11 08:55:00"
  },
  {
    campaign_acceptance_id: 6,
    creator_id: 6,
    campaign_id: 1,
    acceptance_status: "accepted",
    applied_at: "2025-01-22 17:02:00",
    accepted_at: "2025-01-23 11:21:00"
  },
  {
    campaign_acceptance_id: 7,
    creator_id: 7,
    campaign_id: 3,
    acceptance_status: "pending",
    applied_at: "2025-02-01 08:48:00",
    accepted_at: null
  },
  {
    campaign_acceptance_id: 8,
    creator_id: 8,
    campaign_id: 6,
    acceptance_status: "accepted",
    applied_at: "2025-01-28 16:30:00",
    accepted_at: "2025-01-29 10:45:00"
  },
  {
    campaign_acceptance_id: 9,
    creator_id: 9,
    campaign_id: 2,
    acceptance_status: "completed",
    applied_at: "2025-02-03 13:55:00",
    accepted_at: "2025-02-04 09:14:00"
  },
  {
    campaign_acceptance_id: 10,
    creator_id: 10,
    campaign_id: 4,
    acceptance_status: "rejected",
    applied_at: "2025-01-18 19:12:00",
    accepted_at: null
  },
  {
    campaign_acceptance_id: 11,
    creator_id: 2,
    campaign_id: 5,
    acceptance_status: "pending",
    applied_at: "2025-02-06 11:22:00",
    accepted_at: null
  },
  {
    campaign_acceptance_id: 12,
    creator_id: 3,
    campaign_id: 6,
    acceptance_status: "accepted",
    applied_at: "2025-02-07 17:40:00",
    accepted_at: "2025-02-08 12:01:00"
  }
])
