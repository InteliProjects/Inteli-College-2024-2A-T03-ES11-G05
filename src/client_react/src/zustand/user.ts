import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export type TUser = {
    email: string
    access_toke:string
}

type UserStore = {
    user: TUser
    setUser: (user: TUser) => void
    cleanUser: () => void
}

export const useUserStore = create<UserStore>()(
    persist(
      (set) => ({
        user: {     
          email: '',
          access_toke: ''
        },
  
        setUser: (user: TUser) => set({ user }),
  
        cleanUser: () => {
          set({
            user: {
              email: '',
              access_toke: ''
            },
          })
        },
      }),
      {
        name: 'user-cosmetic-co',
        storage: createJSONStorage(() => localStorage),
      },
    ),
  )