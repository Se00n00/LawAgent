import { Component, signal, WritableSignal, effect, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Questioncard } from '../cards/questioncard/questioncard';
import { NewsCards } from '../cards/news-cards/news-cards';
import { SummaryCard } from '../cards/summary-card/summary-card';
import { MainAnswerCard } from '../cards/main-answer-card/main-answer-card';
import { ErrorCard } from '../cards/error-card/error-card';
import { LinkImagesCard } from '../cards/link-images-card/link-images-card';
import { ChartCard } from '../cards/chart-card/chart-card';
import { FormsModule } from '@angular/forms';
import { Supabase } from '../service/supabase';
import { ZeroCard } from '../cards/zero-card/zero-card';
import { ModelErrorCard } from '../cards/model-error-card/model-error-card';
import { Gov } from '../cards/gov/gov';
// import oboe from 'oboe';
import JSONic from 'jsonic';
// @ts-ignore
// import oboe from 'oboe';

declare const clarinet: any;
// // @ts-ignore
// import clarinet from 'clarinet';
// @ts-ignore
declare module 'oboe' {
  const oboe: any;
  export default oboe;
}

// In your component/service
// @ts-ignore
import oboe from 'oboe';

interface output{
  type:string
  content:any
}

@Component({
  selector: 'app-home',
  imports: [
    CommonModule,
    FormsModule,
    RouterLink, 
    Questioncard, 
    NewsCards,
    SummaryCard,
    MainAnswerCard,
    ErrorCard,
    LinkImagesCard,
    ZeroCard,
    ModelErrorCard,
    Gov
  ],
  
  templateUrl: './home.html',
  styleUrl: './home.css'
})

export class Home{
  constructor(public auth:Supabase){}
  // home.component.ts or wherever you use it
  // clarinet: any;

  objectKeys(obj: any): string[] {
    return Object.keys(obj);
  }
  Components:WritableSignal<output[]> = signal([
    {"type":"ZeroCard", "content":""},
    // {"type": "News", "content": [{"title": "Conservation efforts double India's tiger population", "body": "Around three-quarters of the world's tigers now live in India, despite rapidly growing urbanization and human populations. From 2010 to 2022, tigers in India more than doubled from an estimated 1,706 to nearly 3,700, according to a new study published in ...", "article_url": "https://www.msn.com/en-us/news/world/conservation-efforts-double-india-s-tiger-population/ar-AA1z1OTb", "image_url": null, "source": "MSN", "date": "2025-07-22T16:22:00+00:00"}, {"title": "International Tiger Day 2025: Home To 3,682 Tigers, India Now Global Leader In Tiger Conservation", "body": "India has achieved remarkable success in tiger conservation, and it's home to 3,682 large cats, Union Cabinet Minister for Environment, Forests, and Climate Change Bhupender Yadav said on Tuesday. On his X account, Mr Yadav said that India emerged as a ...", "article_url": "https://www.msn.com/en-in/news/india/international-tiger-day-2025-home-to-3-682-tigers-india-now-global-leader-in-tiger-conservation/ar-AA1Ju4co", "image_url": null, "source": "MSN", "date": "2025-07-29T06:55:00+00:00"}]},
    // {"type": "Media", "content": [{"title": "MP dam project will submerge critical tiger corridor: National Tiger ...", "article_url": "https://www.msn.com/en-in/news/India/mp-dam-project-will-submerge-critical-tiger-corridor-national-tiger-conservation-authority/ar-AA1yGBcW", "image_url": "https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AA1yGuRo.img?w=1280&h=720&m=4&q=70"}, {"title": "Tiger conservation pioneer Valmik Thapar dies at 73", "article_url": "https://www.newindianexpress.com/nation/2025/May/31/tiger-conservation-pioneer-valmik-thapar-dies-at-73-2", "image_url": "https://media.assettype.com/newindianexpress/2025-05-31/i5g8oeyy/Valmik-Thapar.jpg?w=640&auto=format,compress&fit=max"}, {"title": "Panna Tiger Reserve Safari Booking Official | Power Traveller", "article_url": "https://powertraveller.com/panna-tiger-reserve-safari-booking-official/", "image_url": "https://powertraveller.com/wp-content/uploads/2024/11/4_panna-tiger-reserve-safari-booking-official.jpg"}, {"title": "TIGER YNY HONG KONG FAN CLUB | 2025\u5e746\u670813\u65e5 \u300a\u4e09\u00b7\u516b\u300b\u9996\u6f14 \u8b1d\u5e55\u6642\u9593 Photo Cr: @siufu ...", "article_url": "https://www.instagram.com/p/DK22ZAlz2Cx/", "image_url": "https://lookaside.instagram.com/seo/google_widget/crawler/?media_id=3654347346253088832"}]},
    // {"type": "Gov", "content": [{"title": "India VNR 2020 - Sustainable Development Goals", "url": "https://www.niti.gov.in/sites/default/files/2022-11/26281VNR-2020-India-Report.pdf", "snippet": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Vitae repudiandae molestiae quibusdam repellendus quia laborum nesciunt eos esse ea dolor quas eveniet sit voluptas, perspiciatis dignissimos error libero quasi? Eius.text-sm overflow-hiddentext-sm overflow-hidden Lorem, ipsum dolor sit amet consectetur adipisicing elit. Vitae repudiandae molestiae quibusdam repellendus quia laborum nesciunt eos esse ea dolor quas eveniet sit voluptas, perspiciatis dignissimos error libero quasi? Eius.text-sm overflow-hiddentext-sm overflow-hidden1 Jun 2020 \u2014 We are honoured to present our second Voluntary National Review and report on the progress made towards fulfilling the 2030 Agenda. India , today ..."}, {"title": "Jal Jeevan Samvad November 2023, Issue-37 English", "url": "https://master-jalshakti-ddws.digifootprint.gov.in/static/uploads/2024/03/JalJeevanSamvad-November-2023-en.pdf", "snippet": "26 Nov 2023 \u2014 Prime Minister Shri Narendra Modi th on 15 August 2019. The programme aims to provide every rural house- hold with affordable and regular."}, {"title": "The Dynamics of Democracy vis-\u00e0-vis Tribal society of ...", "url": "https://printing.arunachal.gov.in/uploads/686b86badf508.pdf", "snippet": "Project Tiger in India . The exhibition, \u201cSilent. Conversation: From Margins ... to Prime Minister Narendra Modi under whose regime since 2014,. Arunachal ..."}, {"title": "ISG NEWSLETTER", "url": "https://prsc.punjab.gov.in/images/Doc/ISG/ISG-Newsletter-DEC-2018.pdf", "snippet": "4 Dec 2018 \u2014 Integrated watershed development programme is one of the major initiatives in the country towards conservation of soil and water resources ..."}]},
    // {"type": "Summeries", "content": {"summeries": [{"heading": "Tiger Population Growth in India", "heading_content": "India's tiger numbers doubled from 1,706 in 2010 to 3,682 in 2022, driven by conservation efforts like Project Tiger, making it home to 75% of global tigers despite urbanization challenges."}, {"heading": "Global Leadership in Conservation", "heading_content": "On International Tiger Day 2025, India leads worldwide tiger protection, hosting three-quarters of wild tigers and setting a model through protected reserves and anti-poaching measures amid habitat threats."}, {"heading": "Sustainable Development Goals (VNR 2020)", "heading_content": "India's 2020 Voluntary National Review highlights progress on UN SDGs, emphasizing holistic economic, social, and environmental advancements as a proactive global contributor to 2030 Agenda targets."}, {"heading": "Jal Jeevan Mission Initiative", "heading_content": "Launched in 2019, this flagship program ensures clean water access to rural households, promoting sanitation, health, and gender equity under SDG 6, with sustained momentum by 2023."}, {"heading": "Tribal Society and Democracy Dynamics", "heading_content": "Under Modi since 2014, policies integrate tribal communities via conservation like Project Tiger and exhibitions, addressing marginalization and fostering inclusive development aligned with SDGs 10 and 15."}, {"heading": "Integrated Watershed Development Program", "heading_content": "This 2018 initiative focuses on soil and water conservation in rural areas, enhancing agriculture resilience, biodiversity, and community participation against climate change under SDGs 2 and 13."}, {"heading": "Ongoing Threats and Calls to Action", "heading_content": "Despite successes, poaching, habitat loss, and human conflicts persist; International Tiger Day urges global collaboration to sustain tiger populations and ecosystem balance for long-term survival."}], "summary_title": "India's Tiger Conservation Successes and Sustainable Development Efforts"}},
    // {"type": "FinalAnswer", "content": {"answer_title": "Tiger Conservation Advances under PM Modi (2023-2025)", "final_answer": "Under PM Narendra Modi, India's tiger population reached 3,682 by 2022, announced in 2025 by Minister Bhupender Yadav, doubling from 2010 and comprising 75% of global tigers. Project Tiger initiatives, protected reserves, and anti-poaching measures drove this success amid urbanization. International Tiger Day 2025 highlighted ongoing efforts, positioning India as a global conservation leader against poaching and habitat loss."}}
  ])
  progress = 0

  MasterQuestion: WritableSignal<string> = signal("")
  Answer: WritableSignal<string> = signal("")


  removeIntro = signal(true)
  askNext = signal(false)

  Searching = signal(false)

  SearchIcon="Icons/add.svg"
  
  // async queryLLM(prompt: string) {
    

  async queryLLM(prompt: string) {
    const res = await fetch(import.meta.env.NG_APP_AGENT_BACKEND, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: prompt })
    });

    // const reader = res.body?.getReader();
    const decoder = new TextDecoder();
    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
    }

    const reader = res.body?.getReader();
    if (!reader) {
        throw new Error('No reader available');
    }
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop()!; // keep last incomplete line

      for (const line of lines) {
          if (!line.trim()) continue; // ✅ Skip empty lines

          try {
              const obj = JSON.parse(line);
              console.log(obj)
              this.Components.update(prev => [...prev, obj]);
              if (obj.type === 'Status') this.progress = obj.content;
          } catch {
              // Plain text message (from AI messages)
              if (line.trim()) { // Only add non-empty messages
                  this.Components.update(prev => [...prev, { 
                      type: 'message', 
                      content: line.trim() 
                  }]);
              }
          }
      }
    }

    // Parse leftover
    if (buffer.trim()) {
        try {
            const obj = JSON.parse(buffer);
            this.Components.update(prev => [...prev, obj]);
            if (obj.type === 'Status'){
              this.progress = obj.content;
            }
        } catch {
            this.Components.update(prev => [...prev, { 
                type: 'message', 
                content: buffer.trim() 
            }]);
        }
    }
  }


  showMainSearchInput(){
    
    if(this.MasterQuestion().length > 0){
        

      // LLM Call
      this.queryLLM(this.MasterQuestion())
      

      this.MasterQuestion.set("")
    }
    this.removeIntro.update((val)=>val = !val)
  }
  receiveMessage(msg: string){
    this.queryLLM(msg)
  }

  newConversation(msg:boolean){
    this.Components.set([{"type":"ZeroCard", "content":""},])
    this.removeIntro.set(true)
  }

  async getExampleContent(content_code: string) {
    try {
      const res = await fetch(import.meta.env.NG_APP_EXAMPLES_JSON+`/${content_code}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });

      this.removeIntro.set(false)
      if (!res.ok) {
        this.Components.set([{"type":"Error","content":res.status}])
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      
      const data = await res.json();
      console.log(data)
      this.Components.set([{"type":"ZeroCard", "content":""}]+data)
    } catch (error) {
      console.error('Error fetching content:', error);
    }
  }

}
