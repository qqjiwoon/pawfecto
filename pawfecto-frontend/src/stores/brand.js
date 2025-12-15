import { ref } from "vue"

export const brands = ref([
  {
    id: 1,
    account_type: "brand",
    username: "pawandco",
    email: "contact@pawandco.com",
    name: "Paw & Co.",
    description: "Premium pet products and handmade items.",
    phone_number: "010-1111-2222",
    profile_image_url: new URL('@/assets/profile1.jpg', import.meta.url).href,
    pet_type: null,
    address: null,
    sns_handle: "@pawandco",
    sns_url: "https://instagram.com/pawandco",
    total_post_count: null,
    follower_count: null,
    style_tags: null
  },
  {
    id: 2,
    account_type: "brand",
    username: "happytail",
    email: "contact@happytail.com",
    name: "Happy Tail",
    description: "Healthy snacks and fun toys for pets.",
    phone_number: "010-3333-4444",
    profile_image_url: new URL('@/assets/profile1.jpg', import.meta.url).href,
    pet_type: null,
    sns_handle: "@happytail",
    sns_url: "https://instagram.com/happytail",
    style_tags: null
  },
  {
    id: 3,
    account_type: "brand",
    username: "petforest",
    email: "hello@petforest.com",
    name: "Pet Forest",
    description: "Nature-inspired toys and accessories.",
    phone_number: "010-5555-6666",
    profile_image_url: new URL('@/assets/profile1.jpg', import.meta.url).href,
    sns_handle: "@petforest",
    sns_url: "https://instagram.com/petforest",
    style_tags: null
  }
])
