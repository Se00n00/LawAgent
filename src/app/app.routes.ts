import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Error } from './error/error';

export const routes: Routes = [
    {path:"", title:"Home", component:Home},
    {path:"**", title:"Page Not Found",component:Error}
];
