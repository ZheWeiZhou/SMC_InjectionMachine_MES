<template>
    <v-row>
        <UperNavbar /> 
    </v-row>    
    <v-row>
        <v-col>
            <div>
                <svg viewBox="0 0 700 312">
                    <defs>
                        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#7DE2FC; stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#B9B6E5; stop-opacity:1" />
                        </linearGradient>
                    </defs>
                    <rect x="0" y="0" width="100%" height="100%" fill="#F4FBF9" />

                    <text fill="#74ACFA"   x="5%" y="8%" font-size="70%" font-weight="bold" text-anchor="middle" >Factory 101 </text>
                    <text fill="#74ACFA"   x="55%" y="8%" font-size="70%" font-weight="bold" text-anchor="middle" >Factory 106 </text>
                    <!-- MULTIPAS-MuCell -->
                    <g :transform="'translate(30, 45)'" @click="selectmachine('MULTIPAS-MuCell')">
                        <path :fill="machinedata['MULTIPAS-MuCell'][0]" d="M1.27 45h11.31l1.91-4.3c.53-1.3 1-2.05 2.23-2.05h23.12c1.22 0 1.44 1 2.23 2.05L44 45h4.59V33.24H1.27zm2.5-9.18h6.93a.82.82 0 0 1 0 1.65H3.77a.82.82 0 0 1 0-1.65m0 2.82h6.93a.71.71 0 1 1 0 1.41H3.77a.71.71 0 1 1 0-1.4ZM2.91 42a.78.78 0 0 1 .78-.78h6.9a.78.78 0 0 1 .78.78v.1a.78.78 0 0 1-.78.78H3.7a.78.78 0 0 1-.78-.78V42Zm5.92-9.69H.62V15.58h8.22v16.75Zm2 0H9.27V15.58h1.56v16.75Zm2.28 0h-1.56V15.58h1.56v16.75Zm7.34 0H18.9V15.58h1.56v16.75Zm2.08 0h-1.85V15.58h1.86v16.75Zm-2.07-14.88H9.27v-1h11.19zm0 14H9.27v-1h11.19zm-8.56-5h-1.31v-5h1.31zm2.1 3.25h-.88v-11.5H14zm4.91 0H18V18.16h.9v11.5Zm19.27-7.88H22.71v-1.15h15.47zm0 5.75H22.71V26.4h15.47v1.16Zm0-1.89H22.71v-3.11h15.47zM44 13.43v2l-1 1v4h-4v-3.81l-1-1.19v-2zM17.86 28.32H16v-8.83h1.81v8.83Zm-2 0h-1.71v-8.83h1.67v8.83Zm9.91-6.24.89.45-1.81 3.58-.89-.45Zm11.33 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm20.65 10.2h-11V20.65h11v11.64ZM48 22.84h-4.31v3.85H48zm-3 4.4h-1.3v.5H45zm1.5 0h-1.31v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3v.5H45zm1.5 0h-1.3v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3V29H45v-.5Zm1.5 0h-1.3V29h1.33v-.5Zm1.5 0h-1.31V29H48v-.5Z" />
                    </g>
                    <!-- <image  @click="selectmachine('MULTIPAS-MuCell')" :href="require('@/assets/machine.png')" x="3%"  y="20%"  width="10%"  height="10%" /> -->
                    <text fill="#121212" x="8%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle">MULTIPAS-MuCell</text>
                    <circle :fill="machinedata['MULTIPAS-MuCell'][0]" class="breathing-circle" cx="6%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['MULTIPAS-MuCell'][0]"  x="8.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['MULTIPAS-MuCell'][1] }}</text> 
                    <text  :fill="machinedata['MULTIPAS-MuCell'][3]"  x="8%" y="18%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['MULTIPAS-MuCell'][2] }}</text>
                    <!-- Engel-120 -->
                    <g :transform="'translate(101, 45)'" @click="selectmachine('Engel-120')">
                        <path :fill="machinedata['Engel-120'][0]" d="M1.27 45h11.31l1.91-4.3c.53-1.3 1-2.05 2.23-2.05h23.12c1.22 0 1.44 1 2.23 2.05L44 45h4.59V33.24H1.27zm2.5-9.18h6.93a.82.82 0 0 1 0 1.65H3.77a.82.82 0 0 1 0-1.65m0 2.82h6.93a.71.71 0 1 1 0 1.41H3.77a.71.71 0 1 1 0-1.4ZM2.91 42a.78.78 0 0 1 .78-.78h6.9a.78.78 0 0 1 .78.78v.1a.78.78 0 0 1-.78.78H3.7a.78.78 0 0 1-.78-.78V42Zm5.92-9.69H.62V15.58h8.22v16.75Zm2 0H9.27V15.58h1.56v16.75Zm2.28 0h-1.56V15.58h1.56v16.75Zm7.34 0H18.9V15.58h1.56v16.75Zm2.08 0h-1.85V15.58h1.86v16.75Zm-2.07-14.88H9.27v-1h11.19zm0 14H9.27v-1h11.19zm-8.56-5h-1.31v-5h1.31zm2.1 3.25h-.88v-11.5H14zm4.91 0H18V18.16h.9v11.5Zm19.27-7.88H22.71v-1.15h15.47zm0 5.75H22.71V26.4h15.47v1.16Zm0-1.89H22.71v-3.11h15.47zM44 13.43v2l-1 1v4h-4v-3.81l-1-1.19v-2zM17.86 28.32H16v-8.83h1.81v8.83Zm-2 0h-1.71v-8.83h1.67v8.83Zm9.91-6.24.89.45-1.81 3.58-.89-.45Zm11.33 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm20.65 10.2h-11V20.65h11v11.64ZM48 22.84h-4.31v3.85H48zm-3 4.4h-1.3v.5H45zm1.5 0h-1.31v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3v.5H45zm1.5 0h-1.3v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3V29H45v-.5Zm1.5 0h-1.3V29h1.33v-.5Zm1.5 0h-1.31V29H48v-.5Z" />
                    </g>                     
                    <!-- <image  @click="selectmachine('Engel-120')" :href="require('@/assets/machine.png')" x="13%"  y="20%"  width="10%"  height="10%" /> -->
                    <text fill="#121212" x="18%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >Engel-120</text>
                    <circle :fill="machinedata['Engel-120'][0]" class="breathing-circle" cx="16%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['Engel-120'][0]"  x="18.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['Engel-120'][1] }}</text>  
                    <text  :fill="machinedata['Engel-120'][3]"  x="18%" y="18%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['Engel-120'][2] }}</text>  
                    <!-- Engel-80 -->
                    <g :transform="'translate(171, 45)'" @click="selectmachine('Engel-80')">
                        <path :fill="machinedata['Engel-80'][0]" d="M1.27 45h11.31l1.91-4.3c.53-1.3 1-2.05 2.23-2.05h23.12c1.22 0 1.44 1 2.23 2.05L44 45h4.59V33.24H1.27zm2.5-9.18h6.93a.82.82 0 0 1 0 1.65H3.77a.82.82 0 0 1 0-1.65m0 2.82h6.93a.71.71 0 1 1 0 1.41H3.77a.71.71 0 1 1 0-1.4ZM2.91 42a.78.78 0 0 1 .78-.78h6.9a.78.78 0 0 1 .78.78v.1a.78.78 0 0 1-.78.78H3.7a.78.78 0 0 1-.78-.78V42Zm5.92-9.69H.62V15.58h8.22v16.75Zm2 0H9.27V15.58h1.56v16.75Zm2.28 0h-1.56V15.58h1.56v16.75Zm7.34 0H18.9V15.58h1.56v16.75Zm2.08 0h-1.85V15.58h1.86v16.75Zm-2.07-14.88H9.27v-1h11.19zm0 14H9.27v-1h11.19zm-8.56-5h-1.31v-5h1.31zm2.1 3.25h-.88v-11.5H14zm4.91 0H18V18.16h.9v11.5Zm19.27-7.88H22.71v-1.15h15.47zm0 5.75H22.71V26.4h15.47v1.16Zm0-1.89H22.71v-3.11h15.47zM44 13.43v2l-1 1v4h-4v-3.81l-1-1.19v-2zM17.86 28.32H16v-8.83h1.81v8.83Zm-2 0h-1.71v-8.83h1.67v8.83Zm9.91-6.24.89.45-1.81 3.58-.89-.45Zm11.33 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm20.65 10.2h-11V20.65h11v11.64ZM48 22.84h-4.31v3.85H48zm-3 4.4h-1.3v.5H45zm1.5 0h-1.31v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3v.5H45zm1.5 0h-1.3v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3V29H45v-.5Zm1.5 0h-1.3V29h1.33v-.5Zm1.5 0h-1.31V29H48v-.5Z" />
                    </g>                        
                    <!-- <image  @click="selectmachine('Engel-80')" :href="require('@/assets/machine.png')" x="23%"  y="20%"  width="10%"  height="10%" /> -->
                    <text fill="#121212" x="28%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >Engel-80</text>
                    <circle :fill="machinedata['Engel-80'][0]" class="breathing-circle" cx="26%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['Engel-80'][0]"  x="28.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['Engel-80'][1] }}</text>
                    <text  :fill="machinedata['Engel-80'][3]"  x="28%" y="18%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['Engel-80'][2] }}</text>             
                    <!-- FCS-Mucell -->
                    <g :transform="'translate(241, 45)'" @click="selectmachine('FCS-Mucell')">
                        <path :fill="machinedata['FCS-Mucell'][0]" d="M1.27 45h11.31l1.91-4.3c.53-1.3 1-2.05 2.23-2.05h23.12c1.22 0 1.44 1 2.23 2.05L44 45h4.59V33.24H1.27zm2.5-9.18h6.93a.82.82 0 0 1 0 1.65H3.77a.82.82 0 0 1 0-1.65m0 2.82h6.93a.71.71 0 1 1 0 1.41H3.77a.71.71 0 1 1 0-1.4ZM2.91 42a.78.78 0 0 1 .78-.78h6.9a.78.78 0 0 1 .78.78v.1a.78.78 0 0 1-.78.78H3.7a.78.78 0 0 1-.78-.78V42Zm5.92-9.69H.62V15.58h8.22v16.75Zm2 0H9.27V15.58h1.56v16.75Zm2.28 0h-1.56V15.58h1.56v16.75Zm7.34 0H18.9V15.58h1.56v16.75Zm2.08 0h-1.85V15.58h1.86v16.75Zm-2.07-14.88H9.27v-1h11.19zm0 14H9.27v-1h11.19zm-8.56-5h-1.31v-5h1.31zm2.1 3.25h-.88v-11.5H14zm4.91 0H18V18.16h.9v11.5Zm19.27-7.88H22.71v-1.15h15.47zm0 5.75H22.71V26.4h15.47v1.16Zm0-1.89H22.71v-3.11h15.47zM44 13.43v2l-1 1v4h-4v-3.81l-1-1.19v-2zM17.86 28.32H16v-8.83h1.81v8.83Zm-2 0h-1.71v-8.83h1.67v8.83Zm9.91-6.24.89.45-1.81 3.58-.89-.45Zm11.33 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm20.65 10.2h-11V20.65h11v11.64ZM48 22.84h-4.31v3.85H48zm-3 4.4h-1.3v.5H45zm1.5 0h-1.31v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3v.5H45zm1.5 0h-1.3v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3V29H45v-.5Zm1.5 0h-1.3V29h1.33v-.5Zm1.5 0h-1.31V29H48v-.5Z" />
                    </g>  
                    <!-- <image  @click="selectmachine('FCS-Mucell')" :href="require('@/assets/machine.png')" x="33%"  y="20%"  width="10%"  height="10%" /> -->
                    <text fill="#121212" x="38%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >FCS-Mucell</text>
                    <circle :fill="machinedata['FCS-Mucell'][0]" class="breathing-circle" cx="36%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['FCS-Mucell'][0]"  x="38.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['FCS-Mucell'][1] }}</text>
                    <text  :fill="machinedata['FCS-Mucell'][3]"  x="38%" y="18%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['FCS-Mucell'][2] }}</text>    
                    <!-- FCS-150 -->
                    <g :transform="'translate(535, 45)'" @click="selectmachine('FCS-150')">
                        <path :fill="machinedata['FCS-150'][0]" d="M1.27 45h11.31l1.91-4.3c.53-1.3 1-2.05 2.23-2.05h23.12c1.22 0 1.44 1 2.23 2.05L44 45h4.59V33.24H1.27zm2.5-9.18h6.93a.82.82 0 0 1 0 1.65H3.77a.82.82 0 0 1 0-1.65m0 2.82h6.93a.71.71 0 1 1 0 1.41H3.77a.71.71 0 1 1 0-1.4ZM2.91 42a.78.78 0 0 1 .78-.78h6.9a.78.78 0 0 1 .78.78v.1a.78.78 0 0 1-.78.78H3.7a.78.78 0 0 1-.78-.78V42Zm5.92-9.69H.62V15.58h8.22v16.75Zm2 0H9.27V15.58h1.56v16.75Zm2.28 0h-1.56V15.58h1.56v16.75Zm7.34 0H18.9V15.58h1.56v16.75Zm2.08 0h-1.85V15.58h1.86v16.75Zm-2.07-14.88H9.27v-1h11.19zm0 14H9.27v-1h11.19zm-8.56-5h-1.31v-5h1.31zm2.1 3.25h-.88v-11.5H14zm4.91 0H18V18.16h.9v11.5Zm19.27-7.88H22.71v-1.15h15.47zm0 5.75H22.71V26.4h15.47v1.16Zm0-1.89H22.71v-3.11h15.47zM44 13.43v2l-1 1v4h-4v-3.81l-1-1.19v-2zM17.86 28.32H16v-8.83h1.81v8.83Zm-2 0h-1.71v-8.83h1.67v8.83Zm9.91-6.24.89.45-1.81 3.58-.89-.45Zm11.33 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm20.65 10.2h-11V20.65h11v11.64ZM48 22.84h-4.31v3.85H48zm-3 4.4h-1.3v.5H45zm1.5 0h-1.31v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3v.5H45zm1.5 0h-1.3v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3V29H45v-.5Zm1.5 0h-1.3V29h1.33v-.5Zm1.5 0h-1.31V29H48v-.5Z" />
                    </g>                       
                    <!-- <image  @click="selectmachine('FCS-150')" :href="require('@/assets/machine.png')" x="75%"  y="20%"  width="10%"  height="10%" /> -->
                    <text fill="#121212" x="80%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >FCS-150</text>
                    <circle :fill="machinedata['FCS-150'][0]" class="breathing-circle" cx="78%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['FCS-150'][0]"  x="80.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['FCS-150'][1] }}</text>
                    <text  :fill="machinedata['FCS-150'][3]"  x="80%" y="18%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['FCS-150'][2] }}</text>  
                    <!-- TOYO -->
                    <g :transform="'translate(605, 45)'" @click="selectmachine('TOYO')">
                        <path :fill="machinedata['TOYO'][0]" d="M1.27 45h11.31l1.91-4.3c.53-1.3 1-2.05 2.23-2.05h23.12c1.22 0 1.44 1 2.23 2.05L44 45h4.59V33.24H1.27zm2.5-9.18h6.93a.82.82 0 0 1 0 1.65H3.77a.82.82 0 0 1 0-1.65m0 2.82h6.93a.71.71 0 1 1 0 1.41H3.77a.71.71 0 1 1 0-1.4ZM2.91 42a.78.78 0 0 1 .78-.78h6.9a.78.78 0 0 1 .78.78v.1a.78.78 0 0 1-.78.78H3.7a.78.78 0 0 1-.78-.78V42Zm5.92-9.69H.62V15.58h8.22v16.75Zm2 0H9.27V15.58h1.56v16.75Zm2.28 0h-1.56V15.58h1.56v16.75Zm7.34 0H18.9V15.58h1.56v16.75Zm2.08 0h-1.85V15.58h1.86v16.75Zm-2.07-14.88H9.27v-1h11.19zm0 14H9.27v-1h11.19zm-8.56-5h-1.31v-5h1.31zm2.1 3.25h-.88v-11.5H14zm4.91 0H18V18.16h.9v11.5Zm19.27-7.88H22.71v-1.15h15.47zm0 5.75H22.71V26.4h15.47v1.16Zm0-1.89H22.71v-3.11h15.47zM44 13.43v2l-1 1v4h-4v-3.81l-1-1.19v-2zM17.86 28.32H16v-8.83h1.81v8.83Zm-2 0h-1.71v-8.83h1.67v8.83Zm9.91-6.24.89.45-1.81 3.58-.89-.45Zm11.33 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm20.65 10.2h-11V20.65h11v11.64ZM48 22.84h-4.31v3.85H48zm-3 4.4h-1.3v.5H45zm1.5 0h-1.31v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3v.5H45zm1.5 0h-1.3v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3V29H45v-.5Zm1.5 0h-1.3V29h1.33v-.5Zm1.5 0h-1.31V29H48v-.5Z" />
                    </g>                         
                    <!-- <image  @click="selectmachine('TOYO')" :href="require('@/assets/machine.png')" x="85%"  y="20%"  width="10%"  height="10%" /> -->
                    <text fill="#121212" x="90%" y="32%" font-size="40%" font-weight="bold" text-anchor="middle" >TOYO</text>
                    <circle :fill="machinedata['TOYO'][0]" class="breathing-circle" cx="88%" cy="35%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['TOYO'][0]"  x="90.5%" y="35.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['TOYO'][1] }}</text>
                    <!-- Tachung -->
                    <g :transform="'translate(535, 186)'" @click="selectmachine('Tachung')">
                        <path :fill="machinedata['Tachung'][0]" d="M1.27 45h11.31l1.91-4.3c.53-1.3 1-2.05 2.23-2.05h23.12c1.22 0 1.44 1 2.23 2.05L44 45h4.59V33.24H1.27zm2.5-9.18h6.93a.82.82 0 0 1 0 1.65H3.77a.82.82 0 0 1 0-1.65m0 2.82h6.93a.71.71 0 1 1 0 1.41H3.77a.71.71 0 1 1 0-1.4ZM2.91 42a.78.78 0 0 1 .78-.78h6.9a.78.78 0 0 1 .78.78v.1a.78.78 0 0 1-.78.78H3.7a.78.78 0 0 1-.78-.78V42Zm5.92-9.69H.62V15.58h8.22v16.75Zm2 0H9.27V15.58h1.56v16.75Zm2.28 0h-1.56V15.58h1.56v16.75Zm7.34 0H18.9V15.58h1.56v16.75Zm2.08 0h-1.85V15.58h1.86v16.75Zm-2.07-14.88H9.27v-1h11.19zm0 14H9.27v-1h11.19zm-8.56-5h-1.31v-5h1.31zm2.1 3.25h-.88v-11.5H14zm4.91 0H18V18.16h.9v11.5Zm19.27-7.88H22.71v-1.15h15.47zm0 5.75H22.71V26.4h15.47v1.16Zm0-1.89H22.71v-3.11h15.47zM44 13.43v2l-1 1v4h-4v-3.81l-1-1.19v-2zM17.86 28.32H16v-8.83h1.81v8.83Zm-2 0h-1.71v-8.83h1.67v8.83Zm9.91-6.24.89.45-1.81 3.58-.89-.45Zm11.33 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm-2.83 0 .89.45-1.81 3.58-.89-.45Zm20.65 10.2h-11V20.65h11v11.64ZM48 22.84h-4.31v3.85H48zm-3 4.4h-1.3v.5H45zm1.5 0h-1.31v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3v.5H45zm1.5 0h-1.3v.5h1.33v-.5Zm1.5 0h-1.31v.5H48zm-3 .65h-1.3V29H45v-.5Zm1.5 0h-1.3V29h1.33v-.5Zm1.5 0h-1.31V29H48v-.5Z" />
                    </g>                     
                    <!-- <image  @click="selectmachine('Tachung')" :href="require('@/assets/machine.png')" x="75%"  y="65%"  width="10%"  height="10%" /> -->
                    <text fill="#121212" x="80%" y="77%" font-size="40%" font-weight="bold" text-anchor="middle" >Tachung</text>
                    <circle :fill="machinedata['Tachung'][0]" class="breathing-circle" cx="78%" cy="80%" r="0.6%" />
                    <text class="breathing-circle" :fill="machinedata['Tachung'][0]"  x="80.5%" y="80.7%" font-size="39%" font-weight="bold" text-anchor="middle" >{{ machinedata['Tachung'][1] }}</text>
                    <text  :fill="machinedata['Tachung'][3]"  x="80%" y="63%" font-size="60%" font-weight="bold" text-anchor="middle" >{{ machinedata['Tachung'][2] }}</text>
                    <!-- WALL -->
                    <line x1="50%"  y1="5%"  x2="50%" y2="95%"  stroke="#DEDEF0" stroke-width="0.15%" />
                    <text fill="#74ACFA"   x="88%" y="99%" font-size="45%" font-weight="bold" text-anchor="middle" >Click the machine icon to view more information </text>
                    <!-- Descript -->
                    <circle fill="#BDBDBD" cx="2%" cy="2%" r="0.6%" />
                    <text fill="#BDBDBD" x="3.7%" y="2.7%" font-size="40%" font-weight="bold" text-anchor="middle" >Stay</text>
                    <circle fill="#4CAF50" cx="6%" cy="2%" r="0.6%" />
                    <text fill="#4CAF50" x="7.7%" y="2.7%" font-size="40%" font-weight="bold" text-anchor="middle" >Work</text>
                    <circle fill="#121212" cx="10%" cy="2%" r="0.6%" />
                    <text fill="#121212" x="12%" y="2.7%" font-size="40%" font-weight="bold" text-anchor="middle" >Offline</text>                
                </svg>
            </div>
        </v-col>
    </v-row>
</template>
  

  <style>
    .breathing-circle {
      animation: breathe 2s infinite ease-in-out;
      transform-origin: center;
    }

    @keyframes breathe {
      0% {
        opacity: 0.5;
      }
      50% {
        opacity: 1;
      }
      100% {
        opacity: 0.5;
      }
    }
    svg g {
      cursor: pointer;
    }
  </style>
  <script>
import axios from 'axios';
import UperNavbar  from './layout/UperNavbar.vue';
  export default {
    name: 'MachineOverviewPage',
    components: {
            UperNavbar
    },
    data: () => ({
        machinedata:{
            "MULTIPAS-MuCell":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "Engel-120":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "Engel-80":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "FCS-Mucell":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "FCS-150":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "TOYO":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
            "Tachung":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
        },
        offlinecolor:"#121212",
        onlinecolor:"rgba(255,196,51,0.6)",
        workcolor: "#4CAF50",
        staycolor:"#BDBDBD",

    }),
    methods: {
        async getmachineonlinestatus(){
            const token = this.$store.getters.getToken;

            // const token = "8d6d4e85-b277-4102-8ffd-defcc7b7b9f9"
            await axios.get(`${this.$store.getters.getHost}/smc/injectionmachinemes/machineconnectstatus`,
            {
                headers:{"accesstoken":token}
            }
            ).then( (response) => {
            if (response.data.status=='error'){
                this.machinedata = {
                    "MULTIPAS-MuCell":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "Engel-120":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "Engel-80":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "FCS-Mucell":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "FCS-150":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "TOYO":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                    "Tachung":["rgba(182,182,180,0.6)","Offline","Sleep","rgba(182,182,180,0.6)"],
                }
            }
            else{
                var res = response.data.Data;
                Object.keys(res).forEach(key => {
                    var machinestatus = res[key]
                    if (machinestatus['Online'] == 'Offline'){
                        console.log("OFFLINE",key)
                        this.machinedata[key] =  ["#000000",'Offline','Sleep',"#000000"];
                    }
                    else{
                        var machinework = machinestatus['Status'].charAt(0).toUpperCase() + machinestatus['Status'].slice(1)
                        var statuscolor = this.staycolor
                        // if (machinework == "Stay"){
                        //     statuscolor = this.staycolor
                        //     this.machinedata[key] =  [this.staycolor,'Online',machinework,this.staycolor];
                        // }
                        if (machinework == "Work"){
                            statuscolor = this.workcolor
                        }
                        this.machinedata[key] =  [statuscolor,'Online',machinework,statuscolor];
                    }
                });
                
            }
        })
        },
        selectmachine(name){
            var machinename = name;
            
            this.$cookies.set('setSelectMachine', machinename, '1d');
            this.$router.push({ name: 'MachineDashboard' });
        }
    },
    mounted(){   
        var token = this.$cookies.get('accesstoken');
        if (!token){
            console.log("Not Login");
            this.$router.push({ name: 'Login' });
        }
        else{
        this.getmachineonlinestatus();
        this.timer=setInterval(this.getmachineonlinestatus,1000);     
        }
    },
    beforeDestory(){
      clearInterval(this.timer);
  },    
  }
</script>
