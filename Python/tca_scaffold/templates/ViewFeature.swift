// MARK: - Reducer

public struct {{ featureName }}: ReducerProtocol {
    public struct State: Equatable {

    }

    public enum Action: BindableAction, Equatable {
        case binding(BindingAction<State>)

    }

    public var body: some ReducerProtocol<State, Action> {
        BindingReducer()
        Reduce<State, Action> { state, action in
            switch action {

            default:
                return .none
            }
        }
    }
}
