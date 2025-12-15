<template>
  <div class="status-wrapper">
    <h2 class="title">Campaign Status</h2>

    <!-- 검색창 -->
    <div class="search-box">
      <input
        v-model="search"
        type="text"
        placeholder="Search Creator..."
        @keyup.enter="filterSearch"
      />
      <button class="search-btn" @click="filterSearch">🔍</button>
    </div>


    <!-- 테이블 -->
    <table class="status-table">
      <thead>
        <tr>
          <th>크리에이터</th>
          <th>업로드 일시</th>
          <th>포스팅 링크</th>
          <th>상태</th>
        </tr>
      </thead>

      <tbody>
        <tr 
          v-for="creator in filteredCreators" 
          :key="creator.id"
        >
          <!-- 크리에이터 정보 -->
          <td>
            <div class="creator-info">
              <img :src="creator.profileImg" class="creator-img" />
              <div>
                <p class="creator-name">{{ creator.name }}</p>
                <p class="creator-handle">@{{ creator.handle }}</p>
              </div>
            </div>
          </td>

          <!-- 업로드 일시 -->
          <td>{{ creator.uploadDate }}</td>

          <!-- 링크 -->
          <td>
            <a :href="creator.postLink" target="_blank">{{ creator.postLink }}</a>
          </td>

          <!-- 상태 -->
          <td>
            <span 
              class="status-tag"
              :class="creator.status.toLowerCase()"
            >
              ● {{ creator.status }}
            </span>
          </td>
        </tr>

        <!-- 검색 결과 없음 -->
        <tr v-if="filteredCreators.length === 0">
          <td colspan="4" class="no-result">찾으시는 크리에이터가 없습니다.</td>
        </tr>

      </tbody>
    </table>

  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import defaultImg from "@/assets/profile1.jpg"

const search = ref("")

// 임시 데이터
const creators = ref([
  {
    id: 1,
    name: "Olivia Rhye",
    handle: "olivia",
    profileImg: defaultImg,
    uploadDate: "2025-11-25",
    postLink: "https://www.instagram.com/asdfaf",
    status: "Complete"
  },
  {
    id: 2,
    name: "Olivia Rhye",
    handle: "olivia",
    profileImg: defaultImg,
    uploadDate: "2025-11-25",
    postLink: "https://www.instagram.com/asdfaf",
    status: "Incomplete"
  },
  {
    id: 3,
    name: "Olivia Rhye",
    handle: "olivia",
    profileImg: defaultImg,
    uploadDate: "2025-11-25",
    postLink: "https://www.instagram.com/asdfaf",
    status: "Complete"
  }
])

// 검색 기능
const filteredCreators = computed(() => {
  if (!search.value) return creators.value
  return creators.value.filter(c =>
    c.name.toLowerCase().includes(search.value.toLowerCase()) ||
    c.handle.toLowerCase().includes(search.value.toLowerCase())
  )
})

function filterSearch() {
  const k = search.value.trim().toLowerCase()

  filteredCreators.value = creators.value.filter(c =>
    c.name.toLowerCase().includes(k) ||
    c.handle.toLowerCase().includes(k)
  )
}

</script>

<style scoped>
.status-wrapper {
  width: 90%;
  max-width: 1200px;
  margin: 40px auto;
  text-align: center;
}

.title {
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  margin: 140px 0 80px 0;
  color: #222;
}

/* 검색창 왼쪽 정렬 */
.search-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 250px;
  background: #fff;
  border: 1px solid #ddd;
  padding: 6px 10px;
  border-radius: 8px;
  margin-left: auto;
  margin-bottom: 20px;
}

.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  padding: 6px 2px;
}

.search-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}


/* 테이블 */
.status-table {
  width: 100%;
  border-collapse: collapse;
}

.status-table th {
  text-align: left;
  padding: 14px;
  color: #444;
  font-size: 14px;
  border-bottom: 1px solid #eee;
}

.status-table td {
  padding: 16px 14px;
  font-size: 14px;
  border-bottom: 1px solid #f2f2f2;
}

/* 크리에이터 정보 */
.creator-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.creator-img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
}

.creator-name {
  font-weight: 600;
}

.creator-handle {
  color: #777;
  font-size: 13px;
}

/* 상태 색상 */
.status-tag {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.status-tag.complete {
  color: #1ea35a;
  background: #e6f7ed;
}

.status-tag.incomplete {
  color: #d93232;
  background: #fdeaea;
}

.no-result {
  text-align: center;
  padding: 20px;
  color: #888;
  font-size: 15px;
}
</style>
