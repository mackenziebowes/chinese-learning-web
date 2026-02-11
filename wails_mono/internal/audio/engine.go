package audio

import "github.com/gen2brain/malgo"

type AudioService struct {
	config malgo.DeviceConfig
}

func NewAudioService() *AudioService {
	return &AudioService{}
}

// StartCapture initializes the mic and logs a message
func (s *AudioService) GetInputDevices() []string {
	return []string{"Built-in Mic", "Native External"}
}
