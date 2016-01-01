run:
	./driver.py

ps: run
	./make_gifs.py

gifs: ps
	./magick.sh

clean:
	rm results/*


