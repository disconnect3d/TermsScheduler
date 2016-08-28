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

    afterEach ->
      $httpBackend.verifyNoOutstandingExpectation()
      $httpBackend.verifyNoOutstandingRequest()

    it 'should show default error', inject((SubjectsService, FlashService) ->
      spy = jasmine.createSpy('Error')
      SubjectsService.Get().then(null,spy)
      $httpBackend.flush()
      $rootScope.$apply()
      expect(spy).toHaveBeenCalledWith(jasmine.any(String))
      return
    )

    it 'should show error from backend', inject((SubjectsService, FlashService) ->
      spy = jasmine.createSpy('Error')
      msg = 'a'
      subjects.respond(400, {message: msg})
      SubjectsService.Get().then(null,spy)
      $httpBackend.flush()
      $rootScope.$apply()
      expect(spy).toHaveBeenCalledWith(msg)
      return
    )

    return
  return