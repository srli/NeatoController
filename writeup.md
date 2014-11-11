#CompRobo Computer Vision Project
Anne and Sophie
11/7/2014

##Project Goal
We wanted to create a way for the Neato to be controlled via hand gestures.  We accomplished this by looking at color filtering.  We created a glove for the user to wear, where each finger is colored a different color.  Then, by looking at the histogram of the image received from the laptop webcam and only filtering for each specific color, we can determine how much of each color is present in the image.  Then, our code filters out background colors to determine whether each finger color is present in the image.  It uses this data to decide what gesture the hand is making, and controls the robot’s motor commands accordingly.

##Design Decision
When we first began this project, we thought we would use some form of keypoint matching to identify the hand within the webcam image and determine its orientation and the gesture it was making.  Early on in the project, we decided instead to work on color filtering, and having each finger a different color in order to track the gesture.  We chose to do this so we could spend more time on looking for multiple gestures and controlling the robot than on finding the hand in the image initially and tracking it.  This design decision greatly simplified the problem of finding the hand in the image.

##Code Structure
Our code is structured as a series of functions that each carry out some function related to reading the hand gestures and controlling the robot.  The code is structured this way because we implemented this project in a very iterative way, first getting color detection working, then checking color existence, then background filtering, and so on.  Because of this, we just added functions as we went.  However, now that it’s complete, it’s pretty clear that it would be better structured in an object-oriented manner.  If we had more time, we would re-structure the code to reflect this better format.  It would be based on a Controller class that had methods to find fingers in an image and translate it into a motor command for the robot.

##Challenges
We had some difficulty figuring out how we wanted to approach the problem at first. While doing some sort of structure analysis of the image would be the most accurate way to find a hand, that would have required a lot of reading into curve finding and haar cascades. We decided to take an easier approach and filter by color, which we had already done a lot of in class. The trade off to this decision is that our project is heavily environment based, and isn’t flexible to different lighting conditions.

We then ran into some challenges.  Because each finger had to be a different color in order to be tracked separately, we had to filter for five different colors.  If we had been filtering for only one color, say, blue, it would have been easy to just run the code on a background for the video that had no blue in it.  But because we needed to look for so many very different colors separately, there was no way to prevent them from showing up in our background, and we ended up getting a lot of false positive readings.  We tried assuming that all colors would have some kind of average threshold, and only if the number of color pixels was above a certain bar would it count as having seen a finger.  This improved the situation somewhat, but it still had a lot of false positive readings.

We eventually solved this problem by filtering the specific background.  We set up code such that the robot reads no gesture input for the first 20 frames of video that it captures.  During these 20 frames, it just reads the background and saves each color histogram separately.  Then, it averages each histogram across those 20 frames to compute an average background value for each color.  Therefore, we have a pretty solid idea on how much of each color is already present in the background.  When we count histograms to determine if a finger is present, all we have to do is check if the histogram value for a color is significantly higher than it was for the background average.  This solution solved a lot of our challenges in terms of determining whether a finger was present and filtering the background.


##Improvement

Our current code simply checks for the existence of a finger, not for it’s position. Because of this, our control scheme is fairly simple, hinging mainly on the combination of fingers one person can hold up. When we tried implementing mean shift, the amount of noise in our background made it difficult to obtain a meaningful mean value. In the future, we could put more time into cleaning up background noise, so that mean shift would return us valuable position data. We could then use these positions to train for gesture recognition.

Moving away from color dependant computer vision to more structural based analysis will allow us to account for a wider range of lighting condition. In a time-unlimited situation, we would ideally build a haar cascade of various hand images and have our code dynamically determine whether the image we’re feeding is a hand or not. This would be a great help in allowing us to find hands without depending on unusual colors and possibly allow us to do gesture recognition.

Additionally, we never really tapped into the possibility of using a Kinect, though it was the inspiration of our project. Our current code operates on 2D plane, and doesn’t really care about the distance of the user’s hand from the camera as long as the color pixels it detects are close enough. However, if we were to implement the Kinect’s depth sensing, we’d be able to have the neato move forward and backwards relative to the hand’s distance. All in all, the Kinect would definitely 

##Lessons Learned

In terms of looking at color filtering and controlling the robot, we found that gaussians we were investigating could be pretty touchy when it came to detecting colors.  We learned how to filter only for the very specific hues we were looking for to prevent false positives from background colors, but not too much, or else we got false negatives from too-harsh filtering.  We learned a lot about different capabilities of using openCV in Python, including histograms, meanshift, gaussians, and integrating with the Neato.

Generally speaking, we realized that it was a good idea for us to build our project from the ground up. Initially, we wanted to start with gesture recognition right away, though that would have required significantly more initial time investment. By realizing that we could start by using what we already knew in color filtering and histograms, we were able to get solid code down rather quickly that we could then build upon. By starting small and working towards the complex, we were able to avoid getting trapped in rabbit holes of complexity and get working project that we could be proud of.