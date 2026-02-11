package main

import (
	"embed"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
	"wails_mono/internal/dictionary"
)

//go:embed all:frontend/dist
var assets embed.FS

func (a *App) StartCapture() string {
	return "Mic check 1-2"
}

func main() {
	// Create an instance of the app structure
	app := NewApp()

	dictSvc, _ := dictionary.NewDictionaryService("data/dictionary.csv")

	// Create application with options
	err := wails.Run(&options.App{
		Title:  "wails-base-fresh",
		Width:  1024,
		Height: 768,
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		BackgroundColour: &options.RGBA{R: 27, G: 38, B: 54, A: 1},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
			dictSvc,
		},
	})

	if err != nil {
		println("Error:", err.Error())
	}
}
