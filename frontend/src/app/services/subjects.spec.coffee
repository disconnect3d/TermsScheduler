describe 'SubjectsService', ->
  describe 'Get()', ->
    $httpBackend = undefined
    $rootScope = undefined
    subjects = undefined

    beforeEach module('TermsScheduler')

    # HOW to mock
    #    beforeEach module('TermsScheduler', ($provide) ->
    #      $provide.value('FlashService', {Error: jasmine.createSpy('Error')})
    #      return
    #    )

    beforeEach inject (_$httpBackend_, _$rootScope_, settings) ->
      $httpBackend = _$httpBackend_
      $rootScope = _$rootScope_

      subjects = $httpBackend.when('GET', settings.backendUrl + 'subjects').respond(400)
      $httpBackend.when('GET', settings.backendUrl + 'subjects_signup').respond(400)

      $httpBackend.when('GET', settings.backendUrl + 'settings').respond({
        "settings": [
          {
            "name": "MAX_PTS_PER_TERM",
            "value": "10"
          },
          {
            "name": "PTS_FOR_ALL",
            "value": "14"
          },
          {
            "name": "PTS_PER_SUB",
            "value": "15"
          },
          {
            "name": "PTS_PER_TERM",
            "value": "10"
          },
          {
            "name": "SUBJECTS_SIGNUP",
            "value": "1"
          },
          {
            "name": "TERMS_SIGNUP",
            "value": "1"
          }
        ]
      })
    # TODO: Make general mock from it

    afterEach ->
      $httpBackend.verifyNoOutstandingExpectation()
      $httpBackend.verifyNoOutstandingRequest()

    it 'should show default error', inject((SubjectsService) ->
      spy = jasmine.createSpy('Error')
      SubjectsService.Get().then(null, spy)
      $httpBackend.flush()
      $rootScope.$apply()
      expect(spy).toHaveBeenCalledWith(jasmine.any(String))
      return
    )

    it 'should show error from backend', inject((SubjectsService) ->
      spy = jasmine.createSpy('Error')
      msg = 'a'
      subjects.respond(400, {message: msg})
      SubjectsService.Get().then(null, spy)
      $httpBackend.flush()
      $rootScope.$apply()
      expect(spy).toHaveBeenCalledWith(msg)
      return
    )

    return
  return