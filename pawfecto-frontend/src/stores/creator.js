import { defineStore } from "pinia"
import axios from "axios"

export const useCreatorStore = defineStore("creator", {
  state: () => ({
    creator: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchCreator(creatorId) {
      this.loading = true
      this.error = null

      const token = localStorage.getItem("access")

      if (!token) {
        this.error = "로그인이 필요합니다."
        this.loading = false
        return
      }

      try {
        const res = await axios.get(
          `http://127.0.0.1:8000/accounts/creator/${creatorId}/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        this.creator = res.data
      } catch (err) {
        console.error(err)
        this.error = "크리에이터 정보를 불러오지 못했습니다."
        this.creator = null
      } finally {
        this.loading = false
      }
    },
  },
})


// import { ref } from "vue"

// export const creators = ref([
//   {
//     "id": 1,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "puppy_daily",
//     "email": "creator1@pawfecto.kr",
//     "account_type": "creator",
//     "name": "강푸름",
//     "phone_number": "010-1234-5678",
//     "pet_type": "dog",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator001/300",
//     "address": "서울특별시 마포구 동교로 45",
//     "sns_handle": "@puppy_daily",
//     "sns_url": "https://www.instagram.com/puppy_daily",
//     "total_post_count": 824,
//     "follower_count": 7238,
//     "following_count": 103,
//     "style_tags": ["wholesome", "cozy", "heartfelt"]
//   },
//   {
//     "id": 2,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "corgi_room",
//     "email": "creator2@pawfecto.kr",
//     "account_type": "creator",
//     "name": "이두부",
//     "phone_number": "010-8877-3321",
//     "pet_type": "dog",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator002/300",
//     "address": "서울특별시 송파구 삼학사로 12",
//     "sns_handle": "@corgi_room",
//     "sns_url": "https://www.instagram.com/corgi_room",
//     "total_post_count": 152,
//     "follower_count": 15300,
//     "following_count": 198,
//     "style_tags": ["funny", "energetic"]
//   },
//   {
//     "id": 3,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "brown_poodle_life",
//     "email": "creator3@pawfecto.kr",
//     "account_type": "creator",
//     "name": "한보리",
//     "phone_number": "010-9911-2334",
//     "pet_type": "dog",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator003/300",
//     "address": "부산광역시 해운대구 재송로 58",
//     "sns_handle": "@brown_poodle_life",
//     "sns_url": "https://www.instagram.com/brown_poodle_life",
//     "total_post_count": 406,
//     "follower_count": 9850,
//     "following_count": 244,
//     "style_tags": ["aesthetic", "minimal"]
//   },
//   {
//     "id": 4,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "happy_shiba_home",
//     "email": "creator4@pawfecto.kr",
//     "account_type": "creator",
//     "name": "서초이",
//     "phone_number": "010-5522-9911",
//     "pet_type": "dog",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator004/300",
//     "address": "경기도 성남시 분당구 판교역로",
//     "sns_handle": "@happy_shiba_home",
//     "sns_url": "https://www.instagram.com/happy_shiba_home",
//     "total_post_count": 312,
//     "follower_count": 18740,
//     "following_count": 167,
//     "style_tags": ["outdoor", "energetic", "funny"]
//   },
//   {
//     "id": 5,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "cat_momo_diary",
//     "email": "creator5@pawfecto.kr",
//     "account_type": "creator",
//     "name": "김모모",
//     "phone_number": "010-4433-1202",
//     "pet_type": "cat",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator005/300",
//     "address": "서울특별시 성북구 동소문로 103",
//     "sns_handle": "@cat_momo_diary",
//     "sns_url": "https://www.instagram.com/cat_momo_diary",
//     "total_post_count": 98,
//     "follower_count": 5400,
//     "following_count": 89,
//     "style_tags": ["calm", "cozy"]
//   },
//   {
//     "id": 6,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "tiny_kitten_world",
//     "email": "creator6@pawfecto.kr",
//     "account_type": "creator",
//     "name": "박솔비",
//     "phone_number": "010-9022-4455",
//     "pet_type": "cat",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator006/300",
//     "address": "대전광역시 유성구 궁동 32",
//     "sns_handle": "@tiny_kitten_world",
//     "sns_url": "https://www.instagram.com/tiny_kitten_world",
//     "total_post_count": 202,
//     "follower_count": 11200,
//     "following_count": 152,
//     "style_tags": ["minimal", "aesthetic"]
//   },
//   {
//     "id": 7,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "paws_and_trails",
//     "email": "creator7@pawfecto.kr",
//     "account_type": "creator",
//     "name": "오훈이",
//     "phone_number": "010-7282-1212",
//     "pet_type": "dog",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator007/300",
//     "address": "제주특별자치도 제주시 애월읍",
//     "sns_handle": "@paws_and_trails",
//     "sns_url": "https://www.instagram.com/paws_and_trails",
//     "total_post_count": 611,
//     "follower_count": 22900,
//     "following_count": 301,
//     "style_tags": ["outdoor", "energetic", "wholesome"]
//   },
//   {
//     "id": 8,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "calm_dog_studio",
//     "email": "creator8@pawfecto.kr",
//     "account_type": "creator",
//     "name": "정하늘",
//     "phone_number": "010-7788-0011",
//     "pet_type": "dog",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator008/300",
//     "address": "서울특별시 강남구 선릉로",
//     "sns_handle": "@calm_dog_studio",
//     "sns_url": "https://www.instagram.com/calm_dog_studio",
//     "total_post_count": 140,
//     "follower_count": 6800,
//     "following_count": 120,
//     "style_tags": ["calm", "minimal"]
//   },
//   {
//     "id": 9,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "maltese_happiness",
//     "email": "creator9@pawfecto.kr",
//     "account_type": "creator",
//     "name": "유하람",
//     "phone_number": "010-2121-8833",
//     "pet_type": "dog",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator009/300",
//     "address": "광주광역시 북구 하남대로",
//     "sns_handle": "@maltese_happiness",
//     "sns_url": "https://www.instagram.com/maltese_happiness",
//     "total_post_count": 321,
//     "follower_count": 13200,
//     "following_count": 221,
//     "style_tags": ["cozy", "heartfelt"]
//   },
//   {
//     "id": 10,
//     "password": "pbkdf2_sha256$demo$hash",
//     "username": "doggo_fun_factory",
//     "email": "creator10@pawfecto.kr",
//     "account_type": "creator",
//     "name": "조두리",
//     "phone_number": "010-9001-6677",
//     "pet_type": "dog",
//     "profile_image": null,
//     "profile_image_url": "https://picsum.photos/seed/creator010/300",
//     "address": "경기도 부천시 중동로",
//     "sns_handle": "@doggo_fun_factory",
//     "sns_url": "https://www.instagram.com/doggo_fun_factory",
//     "total_post_count": 512,
//     "follower_count": 17400,
//     "following_count": 265,
//     "style_tags": ["funny", "energetic", "wholesome"]
//   }
// ]
// )