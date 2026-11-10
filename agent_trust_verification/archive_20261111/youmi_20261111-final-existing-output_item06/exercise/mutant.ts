import {simulateDeliver} from './fixed';
// Known deliberately bad fixture: type assertion bypasses the compiler.
simulateDeliver({kind:'draft',text:'unsafe'} as any);
