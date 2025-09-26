import { Injectable, signal, WritableSignal } from '@angular/core';
import { createClient } from '@supabase/supabase-js'

@Injectable({
  providedIn: 'root'
})
export class Supabase {
  supabase = createClient(import.meta.env.NG_APP_SUPABASE_URL, import.meta.env.NG_APP_SUPABASE_API_KEY)
  sessions:any = null
  outhed = signal(false)
  data:WritableSignal<any> = signal(null) 

  constructor(){
    this.load_session()
  }
  async load_session(){
    const {data} = await this.supabase.auth.getSession()
    let session = data.session
    if(!session){
      const { data:anonData, error:anonError } = await this.supabase.auth.signInAnonymously()
      if(anonError){
        console.error("FAILED TO CREATE ANONMOUS USER",anonError)
      }else{
        session = anonData.session
      }
    }
    this.sessions = session
    this.data.set(session);

    this.supabase.auth.onAuthStateChange((_event,newsession)=>{
      this.sessions = newsession
      this.data.set(newsession);

      // outhed = true if not anonymous
      if (newsession?.user && !newsession.user.is_anonymous) {
        this.outhed.set(true);
      } else {
        this.outhed.set(false);
      }
    })
  }



  async sign_in_oauth(){
    const {data, error} = await this.supabase.auth.signInWithOAuth({
      provider:'google',
      options: {
        redirectTo: import.meta.env.NG_APP_REDIRECT,
      }
    })

    if(error){
      console.log("GOOGLE SIGN IN FAILED", error)
    }else{
      this.outhed.set(true) 
    }
  }

  
  async sign_out() {
    const { error } = await this.supabase.auth.signOut();
    if (error) throw error;
    this.data.set(null)
    this.outhed.set(false)

    const { data: anonData, error: anonError } =
      await this.supabase.auth.signInAnonymously();

    if (anonError) {
      console.error("FAILED TO CREATE ANONMOUS USER AFTER SIGNOUT", anonError);
      this.sessions = null;
    } else {
      this.sessions = anonData.session;
    }

    
  }
}
