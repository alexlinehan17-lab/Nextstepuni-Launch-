declare const PATCH: {
    readonly name: "kobra-ui";
    readonly sounds: {
        readonly tap: {
            readonly source: {
                readonly type: "sine";
                readonly frequency: 1300;
                readonly fm: {
                    readonly ratio: 0.5;
                    readonly depth: 100;
                };
            };
            readonly envelope: {
                readonly attack: 0;
                readonly decay: 0.015;
                readonly sustain: 0;
                readonly release: 0.005;
            };
            readonly gain: 0.2;
        };
        readonly select: {
            readonly source: {
                readonly type: "triangle";
                readonly frequency: {
                    readonly start: 900;
                    readonly end: 780;
                };
            };
            readonly envelope: {
                readonly attack: 0.001;
                readonly decay: 0.055;
            };
            readonly gain: 0.26;
        };
        readonly toggleOn: {
            readonly source: {
                readonly type: "sine";
                readonly frequency: {
                    readonly start: 520;
                    readonly end: 880;
                };
            };
            readonly envelope: {
                readonly attack: 0.002;
                readonly decay: 0.085;
            };
            readonly gain: 0.3;
        };
        readonly toggleOff: {
            readonly source: {
                readonly type: "sine";
                readonly frequency: {
                    readonly start: 780;
                    readonly end: 420;
                };
            };
            readonly envelope: {
                readonly attack: 0.002;
                readonly decay: 0.085;
            };
            readonly gain: 0.28;
        };
        readonly open: {
            readonly source: {
                readonly type: "triangle";
                readonly frequency: {
                    readonly start: 320;
                    readonly end: 620;
                };
            };
            readonly filter: {
                readonly type: "lowpass";
                readonly frequency: 2600;
            };
            readonly envelope: {
                readonly attack: 0.006;
                readonly decay: 0.13;
            };
            readonly gain: 0.24;
        };
        readonly close: {
            readonly source: {
                readonly type: "triangle";
                readonly frequency: {
                    readonly start: 560;
                    readonly end: 300;
                };
            };
            readonly filter: {
                readonly type: "lowpass";
                readonly frequency: 2200;
            };
            readonly envelope: {
                readonly attack: 0.004;
                readonly decay: 0.11;
            };
            readonly gain: 0.22;
        };
        readonly tick: {
            readonly source: {
                readonly type: "square";
                readonly frequency: 1400;
            };
            readonly filter: {
                readonly type: "lowpass";
                readonly frequency: 3000;
            };
            readonly envelope: {
                readonly decay: 0.014;
            };
            readonly gain: 0.1;
        };
        readonly sliderTick: {
            readonly layers: [{
                readonly source: {
                    readonly type: "noise";
                    readonly color: "white";
                };
                readonly filter: {
                    readonly type: "bandpass";
                    readonly frequency: 3000;
                    readonly resonance: 4;
                };
                readonly envelope: {
                    readonly attack: 0;
                    readonly decay: 0.02;
                    readonly sustain: 0;
                    readonly release: 0.006;
                };
                readonly gain: 0.19;
            }, {
                readonly source: {
                    readonly type: "sine";
                    readonly frequency: 700;
                };
                readonly envelope: {
                    readonly attack: 0;
                    readonly decay: 0.012;
                    readonly sustain: 0;
                    readonly release: 0.004;
                };
                readonly gain: 0.09;
            }];
        };
        readonly destructive: {
            readonly layers: [{
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: {
                        readonly start: 300;
                        readonly end: 170;
                    };
                };
                readonly filter: {
                    readonly type: "lowpass";
                    readonly frequency: 1400;
                };
                readonly envelope: {
                    readonly attack: 0.002;
                    readonly decay: 0.12;
                };
                readonly gain: 0.32;
            }, {
                readonly source: {
                    readonly type: "noise";
                    readonly color: "brown";
                };
                readonly filter: {
                    readonly type: "bandpass";
                    readonly frequency: 700;
                    readonly resonance: 1.1;
                };
                readonly envelope: {
                    readonly decay: 0.05;
                };
                readonly gain: 0.06;
            }];
        };
        readonly key: {
            readonly layers: [{
                readonly source: {
                    readonly type: "sine";
                    readonly frequency: {
                        readonly start: 1000;
                        readonly end: 900;
                    };
                };
                readonly envelope: {
                    readonly attack: 0.001;
                    readonly decay: 0.028;
                };
                readonly gain: 0.14;
            }, {
                readonly source: {
                    readonly type: "noise";
                    readonly color: "white";
                };
                readonly filter: {
                    readonly type: "bandpass";
                    readonly frequency: 3200;
                    readonly resonance: 2;
                };
                readonly envelope: {
                    readonly decay: 0.01;
                };
                readonly gain: 0.035;
            }];
        };
        readonly success: {
            readonly layers: [{
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: 784;
                };
                readonly envelope: {
                    readonly attack: 0.004;
                    readonly decay: 0.16;
                };
                readonly gain: 0.22;
            }, {
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: 1175;
                };
                readonly envelope: {
                    readonly attack: 0.004;
                    readonly decay: 0.22;
                };
                readonly gain: 0.18;
                readonly delay: 0.075;
            }];
        };
        readonly error: {
            readonly layers: [{
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: 300;
                };
                readonly filter: {
                    readonly type: "lowpass";
                    readonly frequency: 1200;
                };
                readonly envelope: {
                    readonly attack: 0.003;
                    readonly decay: 0.13;
                };
                readonly gain: 0.26;
            }, {
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: 224;
                };
                readonly filter: {
                    readonly type: "lowpass";
                    readonly frequency: 1000;
                };
                readonly envelope: {
                    readonly attack: 0.003;
                    readonly decay: 0.2;
                };
                readonly gain: 0.24;
                readonly delay: 0.09;
            }];
        };
        readonly warning: {
            readonly layers: [{
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: 622;
                };
                readonly filter: {
                    readonly type: "lowpass";
                    readonly frequency: 2800;
                };
                readonly envelope: {
                    readonly attack: 0.003;
                    readonly decay: 0.14;
                };
                readonly gain: 0.2;
            }, {
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: 622;
                };
                readonly filter: {
                    readonly type: "lowpass";
                    readonly frequency: 2800;
                };
                readonly envelope: {
                    readonly attack: 0.003;
                    readonly decay: 0.18;
                };
                readonly gain: 0.17;
                readonly delay: 0.085;
            }];
        };
        readonly copy: {
            readonly layers: [{
                readonly source: {
                    readonly type: "sine";
                    readonly frequency: 1200;
                };
                readonly envelope: {
                    readonly attack: 0;
                    readonly decay: 0.015;
                    readonly sustain: 0;
                    readonly release: 0.006;
                };
                readonly gain: 0.16;
            }, {
                readonly source: {
                    readonly type: "sine";
                    readonly frequency: 1400;
                };
                readonly envelope: {
                    readonly attack: 0;
                    readonly decay: 0.015;
                    readonly sustain: 0;
                    readonly release: 0.006;
                };
                readonly delay: 0.04;
                readonly gain: 0.14;
            }];
        };
        readonly notification: {
            readonly layers: [{
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: 523;
                };
                readonly envelope: {
                    readonly attack: 0.008;
                    readonly decay: 0.3;
                    readonly sustain: 0.03;
                    readonly release: 0.12;
                };
                readonly gain: 0.14;
            }, {
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: 784;
                };
                readonly envelope: {
                    readonly attack: 0.008;
                    readonly decay: 0.25;
                    readonly sustain: 0.02;
                    readonly release: 0.1;
                };
                readonly delay: 0.12;
                readonly gain: 0.12;
            }];
        };
        readonly swoosh: {
            readonly source: {
                readonly type: "sine";
                readonly frequency: {
                    readonly start: 300;
                    readonly end: 2000;
                };
            };
            readonly envelope: {
                readonly attack: 0.008;
                readonly decay: 0.12;
                readonly sustain: 0;
                readonly release: 0.04;
            };
            readonly gain: 0.12;
        };
        readonly chirp: {
            readonly source: {
                readonly type: "sine";
                readonly frequency: {
                    readonly start: 1200;
                    readonly end: 1500;
                };
            };
            readonly envelope: {
                readonly attack: 0;
                readonly decay: 0.03;
                readonly sustain: 0;
                readonly release: 0.01;
            };
            readonly gain: 0.08;
        };
        readonly command: {
            readonly layers: [{
                readonly source: {
                    readonly type: "triangle";
                    readonly frequency: {
                        readonly start: 1046;
                        readonly end: 784;
                    };
                };
                readonly envelope: {
                    readonly attack: 0.001;
                    readonly decay: 0.075;
                };
                readonly gain: 0.2;
            }, {
                readonly source: {
                    readonly type: "sine";
                    readonly frequency: 1568;
                };
                readonly envelope: {
                    readonly attack: 0.001;
                    readonly decay: 0.045;
                };
                readonly gain: 0.06;
                readonly delay: 0.018;
            }];
        };
        readonly blocked: {
            readonly source: {
                readonly type: "sine";
                readonly frequency: 180;
            };
            readonly filter: {
                readonly type: "lowpass";
                readonly frequency: 700;
            };
            readonly envelope: {
                readonly attack: 0.004;
                readonly decay: 0.06;
            };
            readonly gain: 0.16;
        };
    };
};
export type SoundName = keyof (typeof PATCH)['sounds'];
export declare function setSoundMuted(muted: boolean): void;
export declare function useSoundMuted(): boolean;
export declare function setSoundVolume(volume: number): void;
export declare function useSoundVolume(): number;
export declare function SoundEffects({ children }: {
    children: React.ReactNode;
}): import("react").JSX.Element;
export declare function SoundToggle({ className, onClick, ...props }: React.ComponentProps<'button'>): import("react").JSX.Element;
export {};
