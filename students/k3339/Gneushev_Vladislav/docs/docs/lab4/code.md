## Пути сайта
```
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';

import { Login } from './pages/auth/Login';
import { Register } from './pages/auth/Register';

import { DriversList } from './pages/drivers/DriversList';
import { DriverDetails } from './pages/drivers/DriverDetails';
import { AddDriver } from './pages/drivers/AddDriver';

import { BusesList } from './pages/buses/BusesList';
import { AddBus } from './pages/buses/AddBus';

import { RoutesList } from './pages/routes/RoutesList';
import { AddRoute } from './pages/routes/AddRoute';

import { AssignmentsList } from './pages/assignments/AssignmentsList';
import { AddAssignment } from './pages/assignments/AddAssignment';

import { Profile } from './pages/profile/Profile';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          {/* Auth routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Driver routes */}
          <Route path="/drivers" element={<DriversList />} />
          <Route path="/drivers/:id" element={<DriverDetails />} />
          <Route path="/drivers/add" element={<AddDriver />} />

          {/* Bus routes */}
          <Route path="/buses" element={<BusesList />} />
          <Route path="/buses/add" element={<AddBus />} />

          {/* Route routes */}
          <Route path="/routes" element={<RoutesList />} />
          <Route path="/routes/add" element={<AddRoute />} />

          {/* Assignment routes */}
          <Route path="/assignments" element={<AssignmentsList />} />
          <Route path="/assignments/add" element={<AddAssignment />} />

          {/* Profile route */}
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App; 
```

## Авторизация и токены

### Модуль для управления токеном

Модуль обновляет токен, если он был найден в локальном хранилище. Также он управляет состоянием пользователя, сохраняет данные пользователя

```
import { api } from '@/services/api'

export default {
  namespaced: true,
  
  state: {
    isAuthenticated: false,
    user: null
  },

  mutations: {
    setAuth(state, isAuth) {
      state.isAuthenticated = isAuth
    },
    setUser(state, user) {
      state.user = user
    }
  },

  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/auth/login', credentials)
        localStorage.setItem('token', response.data.token)
        commit('setAuth', true)
        
        const userResponse = await api.get('/users/me')
        commit('setUser', userResponse.data)
        
        return response
      } catch (error) {
        throw error
      }
    },

    async logout({ commit }) {
      localStorage.removeItem('token')
      commit('setAuth', false)
      commit('setUser', null)
    },

    async initAuth({ commit, dispatch }) {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          const response = await api.post('/auth/refresh-token', { token })
          localStorage.setItem('token', response.data.token)
          commit('setAuth', true)
          
          const userResponse = await api.get('/users/me')
          commit('setUser', userResponse.data)
        } catch (error) {
          console.error('Token refresh failed:', error)
          await dispatch('logout')
        }
      } else {
        commit('setAuth', false)
        commit('setUser', null)
      }
    }
  }
} 
```


### Авторизация
```
<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="text-h5 text-center">
            Вход в систему
          </v-card-title>
          
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="form.username"
                label="Имя пользователя"
                prepend-icon="mdi-account"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.password"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                label="Пароль"
                prepend-icon="mdi-lock"
                @click:append="showPassword = !showPassword"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <div class="d-flex flex-column">
                <v-btn
                  color="primary"
                  class="mt-4"
                  type="submit"
                  block
                  :loading="loading"
                  :disabled="!isValid"
                >
                  Войти
                </v-btn>

                <v-btn
                  color="grey"
                  variant="text"
                  class="mt-2"
                  to="/register"
                  block
                >
                  Нет аккаунта? Зарегистрироваться
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>

        <v-snackbar
          v-model="showError"
          color="error"
          timeout="3000"
        >
          {{ errorMessage }}
        </v-snackbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Login',

  data: () => ({
    form: {
      username: '',
      password: ''
    },
    showPassword: false,
    loading: false,
    showError: false,
    errorMessage: ''
  }),

  computed: {
    isValid() {
      return this.form.username && this.form.password
    }
  },

  methods: {
    async handleSubmit() {
      if (!this.isValid) return

      this.loading = true
      try {
        await this.$store.dispatch('auth/login', this.form)
        this.$router.push('/drivers')
      } catch (error) {
        console.error('Login error:', error)
        this.errorMessage = error.response?.data?.detail || 'Ошибка при входе'
        this.showError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 
```


### Регистрация
```
<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="text-h5 text-center">
            Регистрация
          </v-card-title>
          
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="form.username"
                label="Имя пользователя"
                prepend-icon="mdi-account"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.password"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                label="Пароль"
                prepend-icon="mdi-lock"
                @click:append="showPassword = !showPassword"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.confirmPassword"
                :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showConfirmPassword ? 'text' : 'password'"
                label="Подтверждение пароля"
                prepend-icon="mdi-lock-check"
                @click:append="showConfirmPassword = !showConfirmPassword"
                :rules="[
                  v => !!v || 'Обязательное поле',
                  v => v === form.password || 'Пароли не совпадают'
                ]"
                required
              ></v-text-field>

              <div class="d-flex flex-column">
                <v-btn
                  color="primary"
                  class="mt-4"
                  type="submit"
                  block
                  :loading="loading"
                  :disabled="!isValid"
                >
                  Зарегистрироваться
                </v-btn>

                <v-btn
                  color="grey"
                  variant="text"
                  class="mt-2"
                  to="/login"
                  block
                >
                  Уже есть аккаунт? Войти
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>

        <v-snackbar
          v-model="showError"
          color="error"
          timeout="3000"
        >
          {{ errorMessage }}
        </v-snackbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { api } from '@/services/api'

export default {
  name: 'Register',

  data: () => ({
    form: {
      username: '',
      password: '',
      confirmPassword: ''
    },
    showPassword: false,
    showConfirmPassword: false,
    loading: false,
    showError: false,
    errorMessage: ''
  }),

  computed: {
    isValid() {
      return (
        this.form.username &&
        this.form.password &&
        this.form.confirmPassword &&
        this.form.password === this.form.confirmPassword
      )
    }
  },

  methods: {
    async handleSubmit() {
      if (!this.isValid) return

      this.loading = true
      try {
        await api.post('/auth/register', {
          username: this.form.username,
          password: this.form.password
        })
        this.$router.push('/login')
      } catch (error) {
        console.error('Registration error:', error)
        this.errorMessage = error.response?.data?.detail || 'Ошибка при регистрации'
        this.showError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 
```


## Списки сущностей

На примере списка автобусов
```
<template>
  <page-wrapper>
    <div class="mb-4 d-flex justify-space-between align-center">
      <h1 class="text-h4">Список автобусов</h1>
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        to="/buses/add"
      >
        ДОБАВИТЬ АВТОБУС
      </v-btn>
    </div>

    <v-card>
      <v-table hover>
        <thead>
          <tr>
            <th class="text-left pa-4">Гос. номер</th>
            <th class="text-left pa-4">Тип автобуса</th>
            <th class="text-left pa-4">Вместимость</th>
            <th class="text-center pa-4">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bus in buses" :key="bus.id">
            <td class="pa-4">
              <template v-if="editingBus?.id === bus.id">
                <v-text-field
                  v-model="editForm.state_number"
                  density="compact"
                  hide-details
                  :rules="[v => !!v || 'Обязательное поле']"
                ></v-text-field>
              </template>
              <template v-else>
                {{ bus.state_number }}
              </template>
            </td>
            <td class="pa-4">
              <template v-if="editingBus?.id === bus.id">
                <v-select
                  v-model="editForm.bus_type_id"
                  :items="busTypes"
                  item-title="name"
                  item-value="id"
                  density="compact"
                  hide-details
                  :rules="[v => !!v || 'Обязательное поле']"
                ></v-select>
              </template>
              <template v-else>
                {{ bus.bus_type.name }}
              </template>
            </td>
            <td class="pa-4">
              {{ getBusTypeCapacity(bus) }} чел.
            </td>
            <td class="text-center pa-4">
              <template v-if="editingBus?.id === bus.id">
                <v-btn
                  icon
                  variant="text"
                  color="success"
                  class="mr-2"
                  @click="saveEdit"
                  :loading="saving"
                  :disabled="!isValidForm"
                >
                  <v-icon>mdi-check</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  color="error"
                  @click="cancelEdit"
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </template>
              <template v-else>
                <v-btn
                  icon
                  variant="text"
                  color="primary"
                  class="mr-2"
                  @click="startEdit(bus)"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  color="error"
                  @click="confirmDelete(bus)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </td>
          </tr>
        </tbody>
      </v-table>

      <v-overlay
        :model-value="loading"
        class="align-center justify-center"
      >
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-overlay>
    </v-card>

    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы действительно хотите удалить автобус {{ selectedBus?.state_number }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showDeleteDialog = false">
            Отмена
          </v-btn>
          <v-btn 
            color="error" 
            variant="text" 
            @click="deleteBus"
            :loading="deleting"
          >
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
    </v-snackbar>
  </page-wrapper>
</template>

<script>
import { api } from '@/services/api'
import PageWrapper from '@/components/PageWrapper.vue'

export default {
  name: 'BusesList',
  
  components: {
    PageWrapper
  },

  data: () => ({
    buses: [],
    busTypes: [],
    loading: true,
    deleting: false,
    saving: false,
    showDeleteDialog: false,
    showError: false,
    errorMessage: '',
    selectedBus: null,
    editingBus: null,
    editForm: {
      state_number: '',
      bus_type_id: null
    }
  }),

  computed: {
    isValidForm() {
      return this.editForm.state_number && this.editForm.bus_type_id
    }
  },

  async created() {
    await Promise.all([
      this.fetchBuses(),
      this.fetchBusTypes()
    ])
  },

  methods: {
    async fetchBuses() {
      try {
        const { data } = await api.get('/buses')
        this.buses = data
      } catch (error) {
        console.error('Error loading buses:', error)
        this.errorMessage = 'Ошибка при загрузке списка автобусов'
        this.showError = true
      } finally {
        this.loading = false
      }
    },

    async fetchBusTypes() {
      try {
        const { data } = await api.get('/buses/types')
        this.busTypes = data
      } catch (error) {
        console.error('Error loading bus types:', error)
        this.errorMessage = 'Ошибка при загрузке типов автобусов'
        this.showError = true
      }
    },

    getBusTypeCapacity(bus) {
      return bus.bus_type.people_capacity
    },

    startEdit(bus) {
      this.editingBus = bus
      this.editForm = {
        state_number: bus.state_number,
        bus_type_id: bus.bus_type.id
      }
    },

    cancelEdit() {
      this.editingBus = null
      this.editForm = {
        state_number: '',
        bus_type_id: null
      }
    },

    async saveEdit() {
      if (!this.editingBus || !this.isValidForm) return

      this.saving = true
      try {
        await api.put(`/buses/${this.editingBus.id}`, this.editForm)
        await this.fetchBuses()
        this.cancelEdit()
      } catch (error) {
        console.error('Error updating bus:', error)
        this.errorMessage = 'Ошибка при обновлении автобуса'
        this.showError = true
      } finally {
        this.saving = false
      }
    },

    confirmDelete(bus) {
      this.selectedBus = bus
      this.showDeleteDialog = true
    },

    async deleteBus() {
      if (!this.selectedBus) return

      this.deleting = true
      try {
        await api.delete(`/buses/${this.selectedBus.id}`)
        await this.fetchBuses()
        this.showDeleteDialog = false
      } catch (error) {
        console.error('Error deleting bus:', error)
        this.errorMessage = 'Ошибка при удалении автобуса'
        this.showError = true
      } finally {
        this.deleting = false
      }
    }
  }
}
</script> 
```

## Редактирование сущностей

На примере редактирования маршрута
```
<template>
  <v-container class="page-wrapper" fluid>
    <v-row justify="center">
      <v-col cols="12" lg="8" xl="6">
        <div class="mb-4 d-flex justify-space-between align-center">
          <h1 class="text-h4">{{ isEdit ? 'Редактирование маршрута' : 'Добавление маршрута' }}</h1>
        </div>

        <v-card>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="form.name"
                label="Название маршрута"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.start_point_name"
                label="Начальная точка"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.end_point_name"
                label="Конечная точка"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.start_time"
                label="Время начала работы"
                type="time"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.end_time"
                label="Время окончания работы"
                type="time"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model.number="form.interval_seconds"
                label="Интервал (в секундах)"
                type="number"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model.number="form.duration_seconds"
                label="Длительность (в секундах)"
                type="number"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model.number="form.length"
                label="Длина маршрута (км)"
                type="number"
                step="0.1"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <div class="d-flex justify-end mt-4">
                <v-btn
                  color="grey"
                  variant="text"
                  class="mr-4"
                  to="/routes"
                >
                  Отмена
                </v-btn>
                <v-btn
                  color="primary"
                  type="submit"
                  :loading="loading"
                >
                  {{ isEdit ? 'Сохранить' : 'Добавить' }}
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>

        <v-snackbar
          v-model="showError"
          color="error"
          timeout="3000"
        >
          {{ errorMessage }}
        </v-snackbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { api } from '@/services/api'

export default {
  name: 'AddEditRoute',

  data: () => ({
    loading: false,
    showError: false,
    errorMessage: '',
    form: {
      name: '',
      start_point_name: '',
      end_point_name: '',
      start_time: '',
      end_time: '',
      interval_seconds: '',
      duration_seconds: '',
      length: ''
    }
  }),

  computed: {
    isEdit() {
      return !!this.$route.params.id
    }
  },

  async created() {
    if (this.isEdit) {
      await this.fetchRoute()
    }
  },

  methods: {
    async fetchRoute() {
      try {
        const { data } = await api.get(`/routes/${this.$route.params.id}`)
        this.form = {
          name: data.name,
          start_point_name: data.start_point_name,
          end_point_name: data.end_point_name,
          start_time: data.start_time,
          end_time: data.end_time,
          interval_seconds: data.interval_seconds,
          duration_seconds: data.duration_seconds,
          length: data.length
        }
      } catch (error) {
        console.error('Error loading route:', error)
        this.errorMessage = 'Ошибка при загрузке маршрута'
        this.showError = true
        this.$router.push('/routes')
      }
    },

    async handleSubmit() {
      this.loading = true
      try {
        const formData = {
          ...this.form,
          length_km: this.form.length
        }
        delete formData.length

        if (this.isEdit) {
          await api.put(`/routes/${this.$route.params.id}`, formData)
        } else {
          await api.post('/routes', formData)
        }
        this.$router.push('/routes')
      } catch (error) {
        console.error('Error saving route:', error)
        this.errorMessage = 'Ошибка при сохранении маршрута'
        this.showError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 
```

## Удаление сущностей

Происходит при помощи попапа, который показывается при `showDeleteDialog == true`

```
<v-dialog v-model="showDeleteDialog" max-width="400">
    <v-card>
    <v-card-title>Подтверждение удаления</v-card-title>
    <v-card-text>
        Вы действительно хотите удалить этот маршрут?
    </v-card-text>
    <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
        color="grey"
        variant="text"
        @click="showDeleteDialog = false"
        >
        Отмена
        </v-btn>
        <v-btn
        color="error"
        variant="text"
        @click="deleteRoute"
        :loading="deleting"
        >
        Удалить
        </v-btn>
    </v-card-actions>
    </v-card>
</v-dialog>
```
