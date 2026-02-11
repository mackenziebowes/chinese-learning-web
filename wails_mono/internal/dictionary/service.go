package dictionary

import (
	"encoding/csv"
	"os"
	"wails-mono/internal/models"
)

type DictionaryService struct {
	entries []models.Entry
}

func NewDictionaryService(filePath string) (*DictionaryService, error) {
	f, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	lines, err := csv.NewReader(f).ReadAll()
	if err != nil {
		return nil, err
	}

	var entries []models.Entry
	// Skip header (i=1)
	for i := 1; i < len(lines); i++ {
		entries = append(entries, models.Entry{
			Chinese: lines[i][0],
			Pinyin: lines[i][1],
			English: lines[i][2]
		})
	}

	return &DictionaryService{entries: entries}, nil
}

func (s *DictionaryService) Search(query string) []model.Entry {
	return s.entries
}
